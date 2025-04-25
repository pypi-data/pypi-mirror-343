from __future__ import annotations

import json
from typing import Any

from pretix_fattura_elettronica.acubeapi import send_invoice_via_api
from pretix_fattura_elettronica.serializers import InvoiceSerializer
from pretix_fattura_elettronica.utils import create_zip_file, dict_to_xml

from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.views.generic.base import View

from lxml import etree
from pretix.base.models import Invoice, Order
from pretix.control.permissions import (
    EventPermissionRequiredMixin,
    event_permission_required,
    organizer_permission_required,
)
from pretix.control.views.orders import OrderView
from rest_framework import status, viewsets
from rest_framework.decorators import action  # type: ignore
from rest_framework.response import Response

from .forms import OrderChangeElectronicInvoiceForm


class ElectronicInvoiceViewSet(viewsets.ViewSet):
    permission = "can_edit_orders"

    lookup_field = "order_code"

    @action(methods=["POST"], detail=True)
    def update_invoice_information(
        self, request: HttpRequest, order_code: str
    ) -> Response:
        order = get_object_or_404(Order, code=order_code)

        body = request.body.decode("utf-8")
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # we use a form here instead of a serializer because we are reusing
        # the forms fields in the pretix contact form
        form = OrderChangeElectronicInvoiceForm(data=body)

        if form.is_valid():
            meta_info = order.meta_info_data or {}  # type: ignore

            meta_info["pec"] = form.cleaned_data["pec"]
            meta_info["sdi"] = form.cleaned_data["sdi"]
            meta_info["codice_fiscale"] = form.cleaned_data["codice_fiscale"]

            order.meta_info = json.dumps(meta_info)  # type: ignore
            order.save(update_fields=["meta_info"])  # type: ignore

            return Response(
                {"code": order_code},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"errors": dict(form.errors), "other_errors": form.non_field_errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )


@require_http_methods(["POST"])
@organizer_permission_required("can_change_settings")
def send_fattura_elettronica(request, organizer, event, code):
    invoice_id = request.POST.get("invoice_id")

    redirect = HttpResponseRedirect(
        redirect_to=reverse(
            "control:event.order",
            kwargs={"organizer": organizer, "event": event, "code": code},
        )
    )

    if not invoice_id:
        messages.error(request, "Missing invoice_id")

        return redirect

    invoice = Invoice.objects.filter(
        order__code=code, event__slug=event, id=invoice_id
    ).first()

    if not invoice:
        messages.error(request, "Missing invoice")

        return redirect

    try:
        send_invoice_via_api(invoice)
        messages.success(
            request,
            "Fattura elettronica inviata con successo",
        )
    except ValueError as e:
        messages.error(request, str(e))

    return redirect


class EInvoiceInfo(OrderView):
    permission = "can_change_orders"
    template_name = "pretix_fattura_elettronica/change_info.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        context["form"] = OrderChangeElectronicInvoiceForm(
            initial={
                "codice_fiscale": self.object.meta_info_data.get("codice_fiscale"),
                "sdi": self.object.meta_info_data.get("sdi"),
                "pec": self.object.meta_info_data.get("pec"),
            }
        )

        return context

    def post(self, request, *args, **kwargs):
        form = OrderChangeElectronicInvoiceForm(request.POST)

        if form.is_valid():
            meta_info = self.order.meta_info_data or {}

            meta_info["pec"] = form.cleaned_data["pec"]
            meta_info["sdi"] = form.cleaned_data["sdi"]
            meta_info["codice_fiscale"] = form.cleaned_data["codice_fiscale"]

            self.order.meta_info = json.dumps(meta_info)

            self.order.save(update_fields=["meta_info"])

            messages.success(
                request,
                "Updated invoice information",
            )

            return HttpResponseRedirect(
                redirect_to=reverse(
                    "control:event.order",
                    kwargs={
                        "organizer": self.request.event.organizer.slug,
                        "event": self.request.event.slug,
                        "code": self.order.code,
                    },
                )
            )

        messages.error(
            request,
            "There were errors in your form",
        )

        self.object = self.order

        context = self.get_context_data()

        context["form"] = form

        return self.render_to_response(context)


@require_http_methods(["GET"])
@event_permission_required("can_view_orders")
def download_invoice(request, organizer, event, code, invoice):
    invoice = Invoice.objects.filter(
        order__code=code, event__slug=event, id=invoice
    ).first()

    if not invoice:
        raise Http404()

    xml = invoice_to_xml(invoice)

    response = HttpResponse(
        xml,
        content_type="application/xml",
    )

    response["Content-Disposition"] = f"attachment; filename={invoice.number}.xml"

    return response


class EInvoicesAdminView(EventPermissionRequiredMixin, TemplateView):
    permission = "can_view_orders"
    template_name = "pretix_fattura_elettronica/einvoices.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        invoices = (
            Invoice.objects.filter(
                event=self.request.event,
            )
            .select_related("order", "order__event", "order__invoice_address")
            .order_by("-date")
        )

        context["invoices"] = invoices

        return context


def invoice_to_xml(invoice: Invoice) -> str:
    invoice_data = InvoiceSerializer.serialize(invoice).model_dump(by_alias=True)

    NAMESPACE_MAP = {
        "p": "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2",
        "ds": "http://www.w3.org/2000/09/xmldsig#",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }

    SCHEMA_LOCATION = (
        "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2 "
        "http://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2"
        "/Schema_del_file_xml_FatturaPA_versione_1.2.xsd"
    )

    root_tag = "{%s}FatturaElettronica" % NAMESPACE_MAP["p"]
    schema_location_key = "{%s}schemaLocation" % NAMESPACE_MAP["xsi"]

    root = etree.Element(
        root_tag,
        attrib={schema_location_key: SCHEMA_LOCATION},
        nsmap=NAMESPACE_MAP,
        versione="FPR12",
    )

    tags = dict_to_xml(invoice_data)

    for tag in tags:
        root.append(tag)

    return etree.tostring(root, pretty_print=True)


class EInvoicesDownloadAllView(EventPermissionRequiredMixin, View):
    permission = "can_view_orders"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        invoices = (
            Invoice.objects.filter(
                event=self.request.event,
            )
            .select_related("order", "order__event", "order__invoice_address")
            .order_by("-date")
        )

        xmls: dict[str, str] = {}

        for invoice in invoices:
            try:
                xmls[f"{invoice.number}.xml"] = invoice_to_xml(invoice)
            except Exception as e:
                messages.error(
                    request,
                    f"Error with invoice {invoice.number}: {e}",
                )

        zip_file = create_zip_file(xmls)

        return HttpResponse(
            zip_file,
            content_type="application/zip",
        )
