# django urls
from __future__ import annotations

from django.urls import re_path

from pretix.api.urls import router

from . import views

router.register("orders", views.ElectronicInvoiceViewSet, basename="orders")


urlpatterns = [
    re_path(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/orders/(?P<code>[0-9A-Z]+)/send_fattura/$",
        views.send_fattura_elettronica,
        name="send_fattura",
    ),
    re_path(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/e-invoices/$",
        views.EInvoicesAdminView.as_view(),
        name="e-invoices-admin",
    ),
    re_path(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/e-invoices/download$",
        views.EInvoicesDownloadAllView.as_view(),
        name="e-invoices-download-all",
    ),
    re_path(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/orders/(?P<code>[0-9A-Z]+)/e-invoice/(?P<invoice>[0-9A-Z]+).xml$",
        views.download_invoice,
        name="download-invoice",
    ),
    re_path(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/orders/(?P<code>[0-9A-Z]+)/e-invoice/$",
        views.EInvoiceInfo.as_view(),
        name="view-invoice-info",
    ),
]
