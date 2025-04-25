from __future__ import annotations

from decimal import Decimal
import json

from pretix_fattura_elettronica.enums import DOC_TYPE as DT
from pretix_fattura_elettronica.enums import SETTINGS
from pretix_fattura_elettronica.serializers import InvoiceSerializer, OrderSerializer

from django.db.models import Count

import pytest


@pytest.mark.django_db
class TestOrderSerializer:
    def test_serialize_business_order(self, business_order, invoice3):
        ser_invoices = [
            invoice.model_dump(exclude_none=True)
            for _, invoice in OrderSerializer.serialize_invoices(business_order)
        ]
        assert ser_invoices == [
            {
                "fattura_elettronica_header": {
                    "dati_trasmissione": {
                        "id_trasmittente": {
                            "id_paese": "IT",
                            "id_codice": "02053290630",
                        },
                        "codice_destinatario": "1234567",
                        "formato_trasmissione": "FPR12",
                        "progressivo_invio": "DUMMY2-00001",
                    },
                    "cedente_prestatore": {
                        "dati_anagrafici": {
                            "id_fiscale_iva": {
                                "id_paese": "IT",
                                "id_codice": "02053290630",
                            },
                            "codice_fiscale": "94144670489",
                            "anagrafica": {"denominazione": "Python Italia APS"},
                            "regime_fiscale": "RF01",
                        },
                        "sede": {
                            "indirizzo": "Via Roma 11",
                            "cap": "12345",
                            "comune": "Firenze",
                            "nazione": "IT",
                        },
                        "contatti": {"email": "info@python.it"},
                    },
                    "cessionario_committente": {
                        "dati_anagrafici": {
                            "id_fiscale_iva": {"id_paese": "IT", "id_codice": "DE123"},
                            "anagrafica": {"denominazione": "Sample company"},
                        },
                        "sede": {
                            "indirizzo": "Sample company\nJohn Doe\n01020 Napoli\nItaly\nVAT-ID: DE123",
                            "cap": "01020",
                            "comune": "Napoli",
                            "nazione": "IT",
                        },
                    },
                },
                "fattura_elettronica_body": [
                    {
                        "dati_pagamento": {
                            "condizioni_pagamento": "TP02",
                            "dettaglio_pagamento": {
                                "importo_pagamento": "33.25",
                                "modalita_pagamento": "MP08",
                            },
                        },
                        "dati_generali": {
                            "dati_generali_documento": {
                                "tipo_documento": "TD01",
                                "divisa": "EUR",
                                "data": "2017-12-10",
                                "numero": "DUMMY2-00001",
                            }
                        },
                        "dati_beni_servizi": {
                            "dettaglio_linee": [
                                {
                                    "numero_linea": 1,
                                    "descrizione": "Budget Ticket<br />Attendee: Peter",
                                    "prezzo_unitario": "18.85",
                                    "prezzo_totale": "18.85",
                                    "aliquota_iva": "22.00",
                                    "quantita": "1.00",
                                },
                                {
                                    "numero_linea": 2,
                                    "descrizione": "Payment fee",
                                    "prezzo_unitario": "0.20",
                                    "prezzo_totale": "0.20",
                                    "aliquota_iva": "19.00",
                                    "quantita": "1.00",
                                },
                                {
                                    "numero_linea": 3,
                                    "descrizione": "Payment fee",
                                    "prezzo_unitario": "10.00",
                                    "prezzo_totale": "10.00",
                                    "aliquota_iva": "0.00",
                                    "quantita": "1.00",
                                    "natura": "N1",
                                },
                            ],
                            "dati_riepilogo": [
                                {
                                    "aliquota_iva": "22.00",
                                    "imponibile_importo": "18.85",
                                    "imposta": "4.15",
                                },
                                {
                                    "aliquota_iva": "19.00",
                                    "imponibile_importo": "0.20",
                                    "imposta": "0.04",
                                },
                                {
                                    "aliquota_iva": "0.00",
                                    "imponibile_importo": "10.00",
                                    "imposta": "0.00",
                                    "natura": "N1",
                                },
                            ],
                        },
                    }
                ],
            }
        ]

    def test_serialize_private_order(self, private_order, invoice, invoice2):
        ser_invoices = [
            invoice.model_dump(exclude_none=True)
            for _, invoice in OrderSerializer.serialize_invoices(private_order)
        ]
        assert ser_invoices == [
            {
                "fattura_elettronica_header": {
                    "dati_trasmissione": {
                        "id_trasmittente": {
                            "id_paese": "IT",
                            "id_codice": "02053290630",
                        },
                        "codice_destinatario": "0000000",
                        "pec_destinatario": "ciccio@gmail.com",
                        "progressivo_invio": "DUMMY-00001",
                        "formato_trasmissione": "FPR12",
                    },
                    "cedente_prestatore": {
                        "dati_anagrafici": {
                            "id_fiscale_iva": {
                                "id_paese": "IT",
                                "id_codice": "02053290630",
                            },
                            "codice_fiscale": "94144670489",
                            "anagrafica": {"denominazione": "Python Italia APS"},
                            "regime_fiscale": "RF01",
                        },
                        "sede": {
                            "indirizzo": "Via Roma 11",
                            "cap": "12345",
                            "comune": "Firenze",
                            "nazione": "IT",
                        },
                        "contatti": {"email": "info@python.it"},
                    },
                    "cessionario_committente": {
                        "dati_anagrafici": {
                            "codice_fiscale": "COD_FISCALE",
                            "anagrafica": {"nome": "John", "cognome": "Doe"},
                        },
                        "sede": {
                            "indirizzo": "John Doe\n01020 Napoli\nItaly",
                            "cap": "01020",
                            "comune": "Napoli",
                            "nazione": "IT",
                        },
                    },
                },
                "fattura_elettronica_body": [
                    {
                        "dati_pagamento": {
                            "condizioni_pagamento": "TP02",
                            "dettaglio_pagamento": {
                                "importo_pagamento": "33.25",
                                "modalita_pagamento": "MP08",
                            },
                        },
                        "dati_generali": {
                            "dati_generali_documento": {
                                "tipo_documento": "TD01",
                                "divisa": "EUR",
                                "data": "2017-12-10",
                                "numero": "DUMMY-00001",
                            }
                        },
                        "dati_beni_servizi": {
                            "dettaglio_linee": [
                                {
                                    "numero_linea": 1,
                                    "descrizione": "Budget Ticket<br />Attendee: Peter",
                                    "prezzo_unitario": "18.85",
                                    "prezzo_totale": "18.85",
                                    "aliquota_iva": "22.00",
                                    "quantita": "1.00",
                                },
                                {
                                    "numero_linea": 2,
                                    "descrizione": "Payment fee",
                                    "prezzo_unitario": "0.20",
                                    "prezzo_totale": "0.20",
                                    "aliquota_iva": "19.00",
                                    "quantita": "1.00",
                                },
                                {
                                    "numero_linea": 3,
                                    "descrizione": "Payment fee",
                                    "prezzo_unitario": "10.00",
                                    "prezzo_totale": "10.00",
                                    "aliquota_iva": "0.00",
                                    "quantita": "1.00",
                                    "natura": "N1",
                                },
                            ],
                            "dati_riepilogo": [
                                {
                                    "aliquota_iva": "22.00",
                                    "imponibile_importo": "18.85",
                                    "imposta": "4.15",
                                },
                                {
                                    "aliquota_iva": "19.00",
                                    "imponibile_importo": "0.20",
                                    "imposta": "0.04",
                                },
                                {
                                    "aliquota_iva": "0.00",
                                    "imponibile_importo": "10.00",
                                    "imposta": "0.00",
                                    "natura": "N1",
                                },
                            ],
                        },
                    }
                ],
            },
            {
                "fattura_elettronica_header": {
                    "dati_trasmissione": {
                        "id_trasmittente": {
                            "id_paese": "IT",
                            "id_codice": "02053290630",
                        },
                        "codice_destinatario": "0000000",
                        "pec_destinatario": "ciccio@gmail.com",
                        "progressivo_invio": "DUMMY-00002",
                        "formato_trasmissione": "FPR12",
                    },
                    "cedente_prestatore": {
                        "dati_anagrafici": {
                            "id_fiscale_iva": {
                                "id_paese": "IT",
                                "id_codice": "02053290630",
                            },
                            "codice_fiscale": "94144670489",
                            "anagrafica": {"denominazione": "Python Italia APS"},
                            "regime_fiscale": "RF01",
                        },
                        "sede": {
                            "indirizzo": "Via Roma 11",
                            "cap": "12345",
                            "comune": "Firenze",
                            "nazione": "IT",
                        },
                        "contatti": {"email": "info@python.it"},
                    },
                    "cessionario_committente": {
                        "dati_anagrafici": {
                            "codice_fiscale": "COD_FISCALE",
                            "anagrafica": {"nome": "John", "cognome": "Doe"},
                        },
                        "sede": {
                            "indirizzo": "John Doe\n01020 Napoli\nItaly",
                            "cap": "01020",
                            "comune": "Napoli",
                            "nazione": "IT",
                        },
                    },
                },
                "fattura_elettronica_body": [
                    {
                        "dati_pagamento": {
                            "condizioni_pagamento": "TP02",
                            "dettaglio_pagamento": {
                                "importo_pagamento": "33.25",
                                "modalita_pagamento": "MP08",
                            },
                        },
                        "dati_generali": {
                            "dati_generali_documento": {
                                "tipo_documento": "TD01",
                                "divisa": "EUR",
                                "data": "2017-12-10",
                                "numero": "DUMMY-00002",
                            }
                        },
                        "dati_beni_servizi": {
                            "dettaglio_linee": [
                                {
                                    "numero_linea": 1,
                                    "descrizione": "Budget Ticket<br />Attendee: Peter",
                                    "prezzo_unitario": "18.85",
                                    "prezzo_totale": "18.85",
                                    "aliquota_iva": "22.00",
                                    "quantita": "1.00",
                                },
                                {
                                    "numero_linea": 2,
                                    "descrizione": "Payment fee",
                                    "prezzo_unitario": "0.20",
                                    "prezzo_totale": "0.20",
                                    "aliquota_iva": "19.00",
                                    "quantita": "1.00",
                                },
                                {
                                    "numero_linea": 3,
                                    "descrizione": "Payment fee",
                                    "prezzo_unitario": "10.00",
                                    "prezzo_totale": "10.00",
                                    "aliquota_iva": "0.00",
                                    "quantita": "1.00",
                                    "natura": "N1",
                                },
                            ],
                            "dati_riepilogo": [
                                {
                                    "aliquota_iva": "22.00",
                                    "imponibile_importo": "18.85",
                                    "imposta": "4.15",
                                },
                                {
                                    "aliquota_iva": "19.00",
                                    "imponibile_importo": "0.20",
                                    "imposta": "0.04",
                                },
                                {
                                    "aliquota_iva": "0.00",
                                    "imponibile_importo": "10.00",
                                    "imposta": "0.00",
                                    "natura": "N1",
                                },
                            ],
                        },
                    }
                ],
            },
        ]

    def test_retrieve_all_order_invoices(self, private_order):
        ser = OrderSerializer(private_order)

        for left, right in zip(ser._invoices, private_order.invoices.all()):
            assert left == right

    def test_wrong_private_customer_order_data(self, private_order, invoice, invoice2):
        private_order.meta_info_data["codice_fiscale"] = None
        private_order.save()
        with pytest.raises(ValueError) as e:
            OrderSerializer.serialize_invoices(private_order)

        assert str(e.value) == "Codice fiscale is required."

    def test_does_not_need_codice_fiscale_if_not_it(self, private_order, invoice):
        private_order.meta_info_data["codice_fiscale"] = None
        private_order.save()

        invoice.invoice_to_country = "DE"
        invoice.save()

        data = OrderSerializer.serialize_invoices(private_order)

        invoice = data[0][1]

        assert (
            invoice.fattura_elettronica_header.cessionario_committente.dati_anagrafici.codice_fiscale
            is None
        )

    def test_wrong_business_customer_recipient_codice_dest(
        self, business_order, invoice3
    ):
        invoice3.order.meta_info = json.dumps(
            {
                "email": "pec_address",
                "pec": "pec_address",
                "sdi": None,
                "codice_fiscale": "RBTRST82T13F839G",
                "confirm_messages": [],
            }
        )
        invoice3.save()
        data = OrderSerializer.serialize_invoices(business_order)

        assert (
            data[0][1].fattura_elettronica_header.dati_trasmissione.codice_destinatario
            == "0000000"
        )

    def test_no_codice_destinatario_does_not_fail_if_not_it(
        self, business_order, invoice3
    ):
        invoice3.order.meta_info = json.dumps(
            {
                "email": "pec_address",
                "pec": "pec_address",
                "sdi": None,
                "confirm_messages": [],
            }
        )
        invoice3.invoice_to_country = "DE"
        invoice3.save()

        data = OrderSerializer.serialize_invoices(business_order)

        invoice = data[0][1]

        assert (
            invoice.fattura_elettronica_header.dati_trasmissione.codice_destinatario
            == "XXXXXXX"
        )

    @pytest.mark.parametrize(
        "company, name_parts, msg",
        (
            (
                None,
                {},
                "Necessaria denominazione oppure nome e cognome del destinatario.",
            ),
            (
                None,
                {"_scheme": "given_family", "given_name": "John"},
                "In mancanza di Ragione Sociale, nome e cognome non possono esser",
            ),
            (
                None,
                {"_scheme": "given_family", "family_name": "John"},
                "In mancanza di Ragione Sociale, nome e cognome non possono esser",
            ),
        ),
    )
    def test_wrong_recipient_name_or_company_name(
        self, business_order, invoice3, company, name_parts, msg
    ):
        invoice3.invoice_to_company = company
        invoice3.order.invoice_address.name_parts = name_parts
        invoice3.save()
        with pytest.raises(ValueError) as e:
            OrderSerializer.serialize_invoices(business_order)

        assert msg in str(e.value)


@pytest.mark.django_db
class TestInvoiceSerializer:
    def test_invoice_body(self, invoice):
        ser = InvoiceSerializer(invoice)
        lines = invoice.lines.all()
        tax_summary = lines.values(
            "tax_rate",
            "tax_value",
            "gross_value",
        ).annotate(count=Count("tax_rate"))

        assert ser._invoice_body.model_dump(exclude_none=True) == {
            "dati_pagamento": {
                "condizioni_pagamento": "TP02",
                "dettaglio_pagamento": {
                    "importo_pagamento": "33.25",
                    "modalita_pagamento": "MP08",
                },
            },
            "dati_generali": {
                "dati_generali_documento": {
                    "tipo_documento": "TD01",
                    "divisa": invoice.event.currency,
                    "data": "2017-12-10",
                    "numero": invoice.number,
                }
            },
            "dati_beni_servizi": {
                "dettaglio_linee": [
                    {
                        "numero_linea": i + 1,
                        "descrizione": line.description,
                        "prezzo_unitario": str(line.net_value),
                        "prezzo_totale": str(line.net_value),
                        "aliquota_iva": str(line.tax_rate),
                        "quantita": "1.00",
                        **({"natura": "N1"} if line.tax_rate == 0 else {}),
                    }
                    for i, line in enumerate(lines)
                ],
                "dati_riepilogo": [
                    {
                        "aliquota_iva": "22.00",
                        "imponibile_importo": "18.85",
                        "imposta": "4.15",
                    },
                    {
                        "aliquota_iva": "19.00",
                        "imponibile_importo": "0.20",
                        "imposta": "0.04",
                    },
                    {
                        "aliquota_iva": "0.00",
                        "imponibile_importo": "10.00",
                        "imposta": "0.00",
                        "natura": "N1",
                    },
                ],
            },
        }

    def test_invoice_header(self, invoice):
        ser = InvoiceSerializer(invoice)
        assert ser._invoice_header.model_dump(exclude_none=True) == {
            "dati_trasmissione": {
                "id_trasmittente": {
                    "id_paese": invoice.invoice_from_country.code,
                    "id_codice": invoice.invoice_from_vat_id,
                },
                "codice_destinatario": SETTINGS.CODICE_DESTINATARIO_DEFAULT.value,
                "pec_destinatario": json.loads(invoice.order.meta_info).get("pec"),
                "progressivo_invio": invoice.full_invoice_no,
                "formato_trasmissione": "FPR12",
            },
            "cedente_prestatore": {
                "dati_anagrafici": {
                    "id_fiscale_iva": {
                        "id_paese": invoice.invoice_from_country.code,
                        "id_codice": invoice.invoice_from_vat_id,
                    },
                    "anagrafica": {"denominazione": invoice.invoice_from_name},
                    "regime_fiscale": SETTINGS.REGIME_FISCALE.value,
                    "codice_fiscale": SETTINGS.CF.value,
                },
                "sede": {
                    "indirizzo": invoice.invoice_from,
                    "cap": invoice.invoice_from_zipcode,
                    "comune": invoice.invoice_from_city,
                    "nazione": invoice.invoice_from_country.code,
                },
                "contatti": {"email": SETTINGS.EMAIL},
            },
            "cessionario_committente": {
                "dati_anagrafici": {
                    "codice_fiscale": "COD_FISCALE",
                    "anagrafica": {"nome": "John", "cognome": "Doe"},
                },
                "sede": {
                    "indirizzo": invoice.invoice_to,
                    "cap": invoice.invoice_to_zipcode,
                    "comune": invoice.invoice_to_city,
                    "nazione": invoice.invoice_to_country.code,
                },
            },
        }

    def test_complete_private_invoice(self, invoice):
        lines = invoice.lines.all()

        assert InvoiceSerializer.serialize(invoice).model_dump(exclude_none=True) == {
            "fattura_elettronica_header": {
                "dati_trasmissione": {
                    "id_trasmittente": {
                        "id_paese": invoice.invoice_from_country.code,
                        "id_codice": invoice.invoice_from_vat_id,
                    },
                    "codice_destinatario": SETTINGS.CODICE_DESTINATARIO_DEFAULT,
                    "pec_destinatario": json.loads(invoice.order.meta_info).get("pec"),
                    "progressivo_invio": invoice.full_invoice_no,
                    "formato_trasmissione": "FPR12",
                },
                "cedente_prestatore": {
                    "dati_anagrafici": {
                        "id_fiscale_iva": {
                            "id_paese": invoice.invoice_from_country.code,
                            "id_codice": invoice.invoice_from_vat_id,
                        },
                        "anagrafica": {"denominazione": invoice.invoice_from_name},
                        "regime_fiscale": SETTINGS.REGIME_FISCALE.value,
                        "codice_fiscale": SETTINGS.CF.value,
                    },
                    "sede": {
                        "indirizzo": invoice.invoice_from,
                        "cap": invoice.invoice_from_zipcode,
                        "comune": invoice.invoice_from_city,
                        "nazione": invoice.invoice_from_country.code,
                    },
                    "contatti": {"email": SETTINGS.EMAIL.value},
                },
                "cessionario_committente": {
                    "dati_anagrafici": {
                        "codice_fiscale": "COD_FISCALE",
                        "anagrafica": {"nome": "John", "cognome": "Doe"},
                    },
                    "sede": {
                        "indirizzo": invoice.invoice_to,
                        "cap": invoice.invoice_to_zipcode,
                        "comune": invoice.invoice_to_city,
                        "nazione": invoice.invoice_to_country.code,
                    },
                },
            },
            "fattura_elettronica_body": [
                {
                    "dati_pagamento": {
                        "condizioni_pagamento": "TP02",
                        "dettaglio_pagamento": {
                            "importo_pagamento": "33.25",
                            "modalita_pagamento": "MP08",
                        },
                    },
                    "dati_generali": {
                        "dati_generali_documento": {
                            "tipo_documento": DT.TD01,
                            "divisa": invoice.event.currency,
                            "data": "2017-12-10",
                            "numero": invoice.number,
                        }
                    },
                    "dati_beni_servizi": {
                        "dettaglio_linee": [
                            {
                                "numero_linea": i + 1,
                                "descrizione": line.description,
                                "prezzo_unitario": str(line.net_value),
                                "prezzo_totale": str(line.net_value),
                                "aliquota_iva": str(line.tax_rate),
                                "quantita": "1.00",
                                **({"natura": "N1"} if line.tax_rate == 0 else {}),
                            }
                            for i, line in enumerate(lines)
                        ],
                        "dati_riepilogo": [
                            {
                                "aliquota_iva": "22.00",
                                "imponibile_importo": "18.85",
                                "imposta": "4.15",
                            },
                            {
                                "aliquota_iva": "19.00",
                                "imponibile_importo": "0.20",
                                "imposta": "0.04",
                            },
                            {
                                "aliquota_iva": "0.00",
                                "imponibile_importo": "10.00",
                                "imposta": "0.00",
                                "natura": "N1",
                            },
                        ],
                    },
                }
            ],
        }

    def test_complete_business_invoice(self, invoice3):
        invoice = invoice3

        assert InvoiceSerializer.serialize(invoice).model_dump(exclude_none=True) == {
            "fattura_elettronica_header": {
                "dati_trasmissione": {
                    "id_trasmittente": {
                        "id_paese": invoice.invoice_from_country.code,
                        "id_codice": invoice.invoice_from_vat_id,
                    },
                    "codice_destinatario": json.loads(invoice.order.meta_info).get(
                        "sdi"
                    ),
                    "formato_trasmissione": "FPR12",
                    "progressivo_invio": invoice.full_invoice_no,
                },
                "cedente_prestatore": {
                    "dati_anagrafici": {
                        "id_fiscale_iva": {
                            "id_paese": invoice.invoice_from_country.code,
                            "id_codice": invoice.invoice_from_vat_id,
                        },
                        "anagrafica": {"denominazione": invoice.invoice_from_name},
                        "regime_fiscale": SETTINGS.REGIME_FISCALE,
                        "codice_fiscale": SETTINGS.CF,
                    },
                    "sede": {
                        "indirizzo": invoice.invoice_from,
                        "cap": invoice.invoice_from_zipcode,
                        "comune": invoice.invoice_from_city,
                        "nazione": invoice.invoice_from_country.code,
                    },
                    "contatti": {"email": SETTINGS.EMAIL},
                },
                "cessionario_committente": {
                    "dati_anagrafici": {
                        "id_fiscale_iva": {
                            "id_codice": invoice.invoice_to_vat_id,
                            "id_paese": invoice.invoice_to_country.code,
                        },
                        "anagrafica": {"denominazione": invoice.invoice_to_company},
                    },
                    "sede": {
                        "indirizzo": invoice.invoice_to,
                        "cap": invoice.invoice_to_zipcode,
                        "comune": invoice.invoice_to_city,
                        "nazione": invoice.invoice_to_country.code,
                    },
                },
            },
            "fattura_elettronica_body": [
                {
                    "dati_pagamento": {
                        "condizioni_pagamento": "TP02",
                        "dettaglio_pagamento": {
                            "importo_pagamento": "33.25",
                            "modalita_pagamento": "MP08",
                        },
                    },
                    "dati_generali": {
                        "dati_generali_documento": {
                            "tipo_documento": DT.TD01,
                            "divisa": invoice.event.currency,
                            "data": "2017-12-10",
                            "numero": invoice.number,
                        }
                    },
                    "dati_beni_servizi": {
                        "dettaglio_linee": [
                            {
                                "aliquota_iva": "22.00",
                                "descrizione": "Budget Ticket<br />Attendee: Peter",
                                "numero_linea": 1,
                                "prezzo_totale": "18.85",
                                "prezzo_unitario": "18.85",
                                "quantita": "1.00",
                            },
                            {
                                "aliquota_iva": "19.00",
                                "descrizione": "Payment fee",
                                "numero_linea": 2,
                                "prezzo_totale": "0.20",
                                "prezzo_unitario": "0.20",
                                "quantita": "1.00",
                            },
                            {
                                "aliquota_iva": "0.00",
                                "descrizione": "Payment fee",
                                "natura": "N1",
                                "numero_linea": 3,
                                "prezzo_totale": "10.00",
                                "prezzo_unitario": "10.00",
                                "quantita": "1.00",
                            },
                        ],
                        "dati_riepilogo": [
                            {
                                "aliquota_iva": "22.00",
                                "imponibile_importo": "18.85",
                                "imposta": "4.15",
                            },
                            {
                                "aliquota_iva": "19.00",
                                "imponibile_importo": "0.20",
                                "imposta": "0.04",
                            },
                            {
                                "aliquota_iva": "0.00",
                                "imponibile_importo": "10.00",
                                "imposta": "0.00",
                                "natura": "N1",
                            },
                        ],
                    },
                }
            ],
        }
