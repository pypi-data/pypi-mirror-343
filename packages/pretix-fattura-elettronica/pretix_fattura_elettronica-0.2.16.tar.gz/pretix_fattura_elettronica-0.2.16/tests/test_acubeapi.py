from __future__ import annotations

import json

from pretix_fattura_elettronica.acubeapi import (
    send_invoices_via_api,
)
from pretix_fattura_elettronica.serializers import InvoiceSerializer

import httpx
import pytest

from .utils import function_mock


@pytest.fixture(autouse=True)
def auth_token(request):
    return function_mock(
        request,
        "pretix_fattura_elettronica.acubeapi.get_acube_token",
        return_value="buccaccio",
    )


@pytest.mark.django_db
def test_send_invoices_from_order(settings, business_order, invoice3, respx_mock):
    settings.ACUBE_BASE_API_URL = "https://example.dev/api/v1"

    respx_mock.post("https://example.dev/api/v1/invoices").mock(
        return_value=httpx.Response(
            202,
            json={"uuid": "fake-uuid"},
        ),
    )

    resp = send_invoices_via_api(business_order)

    assert resp[0].error is None
    assert resp[0].uuid == "fake-uuid"
    assert resp[0].invoice == invoice3
    assert resp[0].request_body == InvoiceSerializer.serialize(
        invoice3
    ).model_dump_json(exclude_none=True)


@pytest.mark.django_db
def test_send_invoices_from_order_with_error(
    settings, business_order, invoice3, respx_mock
):
    settings.ACUBE_BASE_API_URL = "https://example.dev/api/v1"

    respx_mock.post("https://example.dev/api/v1/invoices").mock(
        return_value=httpx.Response(
            404,
            json={"error": "you're a buccaccio"},
        ),
    )

    resp = send_invoices_via_api(business_order)

    assert resp[0].error == json.dumps(
        {"error": "you're a buccaccio"},
    )
    assert resp[0].uuid is None
    assert resp[0].invoice == invoice3
    assert resp[0].request_body == InvoiceSerializer.serialize(
        invoice3
    ).model_dump_json(exclude_none=True)
