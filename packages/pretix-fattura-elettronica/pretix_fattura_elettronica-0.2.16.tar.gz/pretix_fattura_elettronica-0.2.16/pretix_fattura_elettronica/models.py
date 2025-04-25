from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from pretix.base.models import LoggedModel


class InvoiceLog(LoggedModel):
    invoice = models.ForeignKey(
        "pretixbase.Invoice",
        verbose_name=_("Fattura Log Invio"),
        on_delete=models.CASCADE,
    )
    request_body = models.JSONField()
    uuid = models.CharField(max_length=32, null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
