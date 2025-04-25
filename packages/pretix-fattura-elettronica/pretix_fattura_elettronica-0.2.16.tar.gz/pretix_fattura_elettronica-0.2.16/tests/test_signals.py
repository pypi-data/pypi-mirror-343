from __future__ import annotations

from unittest.mock import patch

import pytest
from pretix.base.models import Event, Order
from pretix.base.signals import order_paid

from .utils import instance_mock


@pytest.mark.django_db
@patch("pretix_fattura_elettronica.signals.invoices.send_invoices_via_api")
def test_send_invoice_called(mock_sig, request, settings):
    with patch(
        "pretix_fattura_elettronica.signals.invoices.fattura_elettronica_sender"
    ) as mock_send_invoice:
        settings.ENABLE_INVOICE_AUTOSEND = True
        event = Event(pk="pk", name="PyConIT", plugins="pretix_fattura_elettronica")
        order = instance_mock(request, Order)
        order.event = event
        order_paid.connect(mock_send_invoice, dispatch_uid="fattura_elt")
        order_paid.send(order.event, order=order)

    mock_sig.assert_called_once_with(order)
