from __future__ import annotations

from pretix_fattura_elettronica.models import InvoiceLog

from django import template

register = template.Library()


@register.filter
def einvoice_sent(invoice):
    counter = InvoiceLog.objects.filter(invoice=invoice, uuid__isnull=False).count()
    return counter > 0


@register.simple_tag
def check_invoices(order):
    return "merda"
