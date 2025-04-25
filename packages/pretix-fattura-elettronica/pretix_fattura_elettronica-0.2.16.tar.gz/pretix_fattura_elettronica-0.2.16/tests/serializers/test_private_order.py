from __future__ import annotations

import datetime
import json
from decimal import Decimal

from pretix_fattura_elettronica.serializers import InvoiceSerializer

import pytest
import time_machine
from django_countries.fields import Country
from pretix.base.models import (
    Event,
    Invoice,
    InvoiceAddress,
    Order,
    OrderPosition,
    TaxRule,
)
from pretix.base.services.invoices import build_invoice, generate_cancellation

pytestmark = pytest.mark.django_db


@pytest.fixture
def tax_rule_ticket(event):
    return event.tax_rules.create(rate=Decimal("19.00"))


@pytest.fixture
def tax_rule_hotel(event):
    return event.tax_rules.create(rate=Decimal("0.00"), name="N1")


@pytest.fixture
def tax_rule_membership(event):
    return event.tax_rules.create(rate=Decimal("0.00"), name="N2.2")


def get_private_order(
    event: Event,
    tax_rule_ticket: TaxRule,
    tax_rule_hotel: TaxRule,
    tax_rule_membership: TaxRule,
):
    codice_destinatario = "000000"
    pec_address = "ciccio@gmail.com"

    now = datetime.datetime.now(datetime.timezone.utc)

    o = Order.objects.create(
        code="FOO",
        event=event,
        email="dummy@dummy.test",
        status=Order.STATUS_PENDING,
        secret="k24fiuwvu8kxz3y1",
        datetime=now,
        expires=now + datetime.timedelta(days=9),
        total=23,
        locale="en",
        meta_info=json.dumps(
            {
                "email": pec_address,
                "pec": pec_address,
                "codice_fiscale": "cod_fiscale",
                "sdi": codice_destinatario,
            }
        ),
    )

    o.payments.create(
        state="confirmed",
        amount=23,
        provider="stripe",
        payment_date=now,
    )

    InvoiceAddress.objects.create(
        order=o,
        company="",
        name_parts={
            "_scheme": "given_family",
            "given_name": "A very long name",
            "family_name": "A very long family name",
        },
        country=Country("IT"),
        # using a German address to test the truncation of the address
        city="Berlin",
        zipcode="10234",
        street="Koppenstraße 8",
        vat_id="",
        vat_id_validated=True,
        is_business=False,
    )

    # Tickets

    ticket_item = event.items.create(
        name="Ticket", default_price=23, tax_rule=tax_rule_ticket
    )

    OrderPosition.objects.create(
        order=o,
        item=ticket_item,
        variation=None,
        price=Decimal("23"),
        attendee_name_parts={"full_name": "Peter", "_scheme": "full"},
        secret="z3fsn8jyufm5kpk768q69gkbyr5f4h6w",
        pseudonymization_id="ABCDEFGHKL",
        positionid=1,
    )

    OrderPosition.objects.create(
        order=o,
        item=ticket_item,
        variation=None,
        price=Decimal("23"),
        attendee_name_parts={"full_name": "Pietro", "_scheme": "full"},
        secret="z3fsn8jyufm5kpk768q69gkbyr5f4h6w",
        pseudonymization_id="ABCDEFGHKL2",
        positionid=1,
    )

    # Membership

    membership_item = event.items.create(
        name="Membership", default_price=10, tax_rule=tax_rule_membership
    )

    OrderPosition.objects.create(
        order=o,
        item=membership_item,
        variation=None,
        price=Decimal("10.00"),
        attendee_name_parts={"full_name": "Peter", "_scheme": "full"},
        secret="z3fsn8jyufm5kpk768q69gkbyr5f4h6w",
        pseudonymization_id="SomethingElse",
        positionid=2,
    )

    # Hotel

    hotel_item = event.items.create(
        name="Hotel", default_price=100, tax_rule=tax_rule_hotel
    )

    OrderPosition.objects.create(
        order=o,
        item=hotel_item,
        variation=None,
        price=Decimal("100.00"),
        attendee_name_parts={"full_name": "Peter", "_scheme": "full"},
        secret="z3fsn8jyufm5kpk768q69gkbyr5f4h6w",
        pseudonymization_id="SomethingElseHotel",
        positionid=3,
    )

    return o


@pytest.fixture
@time_machine.travel("2017-12-01T10:00:00Z")
def private_order(
    event: Event,
    tax_rule_ticket: TaxRule,
    tax_rule_hotel: TaxRule,
    tax_rule_membership: TaxRule,
):
    return get_private_order(
        event, tax_rule_ticket, tax_rule_hotel, tax_rule_membership
    )


@pytest.fixture
@time_machine.travel("2017-12-01T10:00:00Z")
def private_order_legacy_tax_rules(
    event: Event,
    tax_rule_ticket: TaxRule,
):
    tax_rule_zero = event.tax_rules.create(rate=Decimal("0.00"))

    return get_private_order(
        event,
        tax_rule_ticket,
        tax_rule_hotel=tax_rule_zero,
        tax_rule_membership=tax_rule_zero,
    )


@pytest.fixture
@time_machine.travel("2017-12-01T10:00:00Z")
def private_invoice(private_order: Order):
    invoice = Invoice(
        order=private_order,
        event=private_order.event,
        organizer=private_order.event.organizer,
        date=datetime.datetime.now(private_order.event.timezone).date(),
    )
    invoice.event.settings["invoice_address_from"] = "Via Roma 11"
    invoice.event.settings["invoice_address_from_name"] = "Python Italia APS"
    invoice.event.settings["invoice_address_from_zipcode"] = "12345"
    invoice.event.settings["invoice_address_from_city"] = "Firenze"
    invoice.event.settings["invoice_address_from_country"] = str(Country("IT"))
    invoice.event.settings["invoice_address_from_vat_id"] = "02053290630"
    invoice.save()
    invoice = build_invoice(invoice)
    if private_order.status == Order.STATUS_CANCELED:
        generate_cancellation(invoice, False)

    return invoice


@pytest.fixture
@time_machine.travel("2017-12-01T10:00:00Z")
def private_invoice_legacy_tax_rules(private_order_legacy_tax_rules: Order):
    invoice = Invoice(
        order=private_order_legacy_tax_rules,
        event=private_order_legacy_tax_rules.event,
        organizer=private_order_legacy_tax_rules.event.organizer,
        date=datetime.datetime.now(
            private_order_legacy_tax_rules.event.timezone
        ).date(),
    )
    invoice.event.settings["invoice_address_from"] = "Via Roma 11"
    invoice.event.settings["invoice_address_from_name"] = "Python Italia APS"
    invoice.event.settings["invoice_address_from_zipcode"] = "12345"
    invoice.event.settings["invoice_address_from_city"] = "Firenze"
    invoice.event.settings["invoice_address_from_country"] = str(Country("IT"))
    invoice.event.settings["invoice_address_from_vat_id"] = "02053290630"
    invoice.save()
    invoice = build_invoice(invoice)
    if private_order_legacy_tax_rules.status == Order.STATUS_CANCELED:
        generate_cancellation(invoice, False)

    return invoice


@pytest.fixture
def serialized_invoice(private_invoice: Invoice):
    return InvoiceSerializer.serialize(private_invoice).model_dump()


@pytest.fixture
def serialized_invoice_legacy_tax_rules(private_invoice_legacy_tax_rules: Invoice):
    return InvoiceSerializer.serialize(private_invoice_legacy_tax_rules).model_dump()


def test_header(serialized_invoice: dict):
    assert serialized_invoice["fattura_elettronica_header"] == {
        "dati_trasmissione": {
            "id_trasmittente": {"id_paese": "IT", "id_codice": "02053290630"},
            "progressivo_invio": "DUMMY-00001",
            "formato_trasmissione": "FPR12",
            "codice_destinatario": "000000",
            "pec_destinatario": "ciccio@gmail.com",
        },
        "cedente_prestatore": {
            "dati_anagrafici": {
                "id_fiscale_iva": {"id_paese": "IT", "id_codice": "02053290630"},
                "codice_fiscale": "94144670489",
                "anagrafica": {
                    "denominazione": "Python Italia APS",
                    "nome": None,
                    "cognome": None,
                    "titolo": None,
                    "cod_eori": None,
                },
                "regime_fiscale": "RF01",
            },
            "sede": {
                "indirizzo": "Via Roma 11",
                "numero_civico": None,
                "cap": "12345",
                "comune": "Firenze",
                "provincia": None,
                "nazione": "IT",
            },
            "contatti": {"telefono": None, "fax": None, "email": "info@python.it"},
        },
        "cessionario_committente": {
            "dati_anagrafici": {
                "id_fiscale_iva": None,
                "codice_fiscale": "COD_FISCALE",
                "anagrafica": {
                    "denominazione": None,
                    "nome": "A very long name A very long family",
                    "cognome": "name",
                    "titolo": None,
                    "cod_eori": None,
                },
            },
            "sede": {
                "indirizzo": "A very long name A very long family name\nKoppenstrasse 8\n102",
                "numero_civico": None,
                "cap": "10234",
                "comune": "Berlin",
                "provincia": None,
                "nazione": "IT",
            },
        },
    }

    # make sure that length of the address is max 60
    assert (
        len(
            serialized_invoice["fattura_elettronica_header"]["cessionario_committente"][
                "sede"
            ]["indirizzo"]
        )
        <= 60
    )


@pytest.mark.parametrize(
    "invoice_name",
    ["serialized_invoice", "serialized_invoice_legacy_tax_rules"],
)
def test_body_legacy_tax_rules(request, invoice_name):
    invoice = request.getfixturevalue(invoice_name)

    assert invoice["fattura_elettronica_body"] == [
        {
            "dati_generali": {
                "dati_generali_documento": {
                    "tipo_documento": "TD01",
                    "divisa": "EUR",
                    "data": "2017-12-01",
                    "numero": "DUMMY-00001",
                }
            },
            "dati_beni_servizi": {
                "dettaglio_linee": [
                    {
                        "numero_linea": 1,
                        "descrizione": "Ticket<br />Attendee: Peter",
                        "quantita": "1.00",
                        "unita_misura": None,
                        "prezzo_unitario": "19.33",
                        "prezzo_totale": "19.33",
                        "aliquota_iva": "19.00",
                        "ritenuta": None,
                        "natura": None,
                    },
                    {
                        "numero_linea": 2,
                        "descrizione": "Ticket<br />Attendee: Pietro",
                        "quantita": "1.00",
                        "unita_misura": None,
                        "prezzo_unitario": "19.33",
                        "prezzo_totale": "19.33",
                        "aliquota_iva": "19.00",
                        "ritenuta": None,
                        "natura": None,
                    },
                    {
                        "numero_linea": 3,
                        "descrizione": "Membership<br />Attendee: Peter",
                        "quantita": "1.00",
                        "unita_misura": None,
                        "prezzo_unitario": "10.00",
                        "prezzo_totale": "10.00",
                        "aliquota_iva": "0.00",
                        "ritenuta": None,
                        "natura": "N2.2",
                    },
                    {
                        "numero_linea": 4,
                        "descrizione": "Hotel<br />Attendee: Peter",
                        "quantita": "1.00",
                        "unita_misura": None,
                        "prezzo_unitario": "100.00",
                        "prezzo_totale": "100.00",
                        "aliquota_iva": "0.00",
                        "ritenuta": None,
                        "natura": "N1",
                    },
                ],
                "dati_riepilogo": [
                    {
                        "aliquota_iva": "19.00",
                        "natura": None,
                        "imponibile_importo": "38.66",
                        "imposta": "7.35",
                    },
                    {
                        "aliquota_iva": "0.00",
                        "natura": "N2.2",
                        "imponibile_importo": "10.00",
                        "imposta": "0.00",
                    },
                    {
                        "aliquota_iva": "0.00",
                        "natura": "N1",
                        "imponibile_importo": "100.00",
                        "imposta": "0.00",
                    },
                ],
            },
            "dati_pagamento": {
                "condizioni_pagamento": "TP02",
                "dettaglio_pagamento": {
                    "importo_pagamento": "156.00",
                    "modalita_pagamento": "MP08",
                },
            },
        }
    ]
