from __future__ import annotations

from typing import Any, TypedDict
from typing_extensions import Unpack

from pretix_fattura_elettronica.acubeapi import send_invoices_via_api

from django.conf import settings
from django.dispatch import receiver

from pretix.base.models import Order
from pretix.base.signals import order_paid


class OrderPaidSignalKwargs(TypedDict):
    order: Order


@receiver(order_paid, dispatch_uid="fattura_elt")
def fattura_elettronica_sender(sender: Any, **kwargs: Unpack[OrderPaidSignalKwargs]):
    if getattr(settings, "ENABLE_INVOICE_AUTOSEND", False):
        send_invoices_via_api(kwargs.get("order"))
