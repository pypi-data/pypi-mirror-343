from __future__ import annotations

import json

from django.conf import settings

import httpx

from .models import InvoiceLog
from .serializers import InvoiceSerializer, OrderSerializer


def get_acube_token():
    headers = {"Content-type": "application/json"}
    body = json.dumps(
        {"email": settings.ACUBE_USERNAME, "password": settings.ACUBE_PWD}
    )
    resp = httpx.post(
        f"{settings.ACUBE_COMMON_API_URL}/login", data=body, headers=headers
    )

    resp.raise_for_status()

    return resp.json().get("token")


def send_invoice(invoice_payload, token):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    url = f"{settings.ACUBE_BASE_API_URL}/invoices"
    response = httpx.post(url, json=json.loads(invoice_payload), headers=headers)
    return response


def save_invoice_log(inv_obj, ser_invoice, response: httpx.Response):
    log_entry = InvoiceLog.objects.create(
        invoice=inv_obj,
        request_body=ser_invoice.model_dump_json(exclude_none=True),
        uuid=response.json()["uuid"] if response.is_success else None,
        error=response.text if not response.is_success else None,
    )
    return log_entry


def send_invoices_via_api(order):
    ser_invoices = OrderSerializer.serialize_invoices(order)
    token = get_acube_token()
    invoices_data = []
    for inv_obj, ser_invoice in ser_invoices:
        send_res = send_invoice(ser_invoice.model_dump_json(exclude_none=True), token)
        log_entry = save_invoice_log(inv_obj, ser_invoice, send_res)
        invoices_data.append(log_entry)
    return invoices_data


def send_invoice_via_api(invoice):
    counter = InvoiceLog.objects.filter(invoice=invoice, uuid__isnull=False).count()

    if counter > 0:
        raise ValueError("Invoice already sent!")

    ser_invoice = InvoiceSerializer.serialize(invoice)

    send_res = send_invoice(
        ser_invoice.model_dump_json(exclude_none=True), get_acube_token()
    )

    log_entry = save_invoice_log(invoice, ser_invoice, send_res)

    if log_entry.error:
        raise ValueError(
            f"Something went wrong during the API call. Error: {log_entry.error}"
        )

    return log_entry
