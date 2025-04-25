from __future__ import annotations

import json
from typing import Any

from pretix_fattura_elettronica.forms import ElectronicInvoiceForm

from django.dispatch import receiver

from pretix.base.models import Order
from pretix.base.signals import order_placed
from pretix.presale.signals import contact_form_fields


@receiver(contact_form_fields, dispatch_uid="fattura_elt")
def add_fields_to_contact_form_fields(sender: Any, **kwargs: Any):
    return ElectronicInvoiceForm.declared_fields


@receiver(order_placed, dispatch_uid="fattura_elt")
def update_meta(sender: Any, order: Order, **kwargs: Any):
    # Pretix saves the data from the form above inside a `contact_form_data`
    # key in the meta_info field. We need to move it to the root of the
    # meta_info field to make it work with the rest of the plugin.

    meta_data = order.meta_info_data or {}

    if "contact_form_data" in meta_data:
        contact_form_data = meta_data["contact_form_data"]
        meta_data["pec"] = contact_form_data.get("pec")
        meta_data["sdi"] = contact_form_data.get("sdi")
        meta_data["codice_fiscale"] = contact_form_data.get("codice_fiscale")

    order.meta_info = json.dumps(meta_data)
    order.save(update_fields=["meta_info"])
