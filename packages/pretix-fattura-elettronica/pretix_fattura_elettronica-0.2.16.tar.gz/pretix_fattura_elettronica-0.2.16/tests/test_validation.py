from __future__ import annotations

from unittest.mock import ANY

from pretix_fattura_elettronica.serializers import DatiRiepilogo, DettaglioLinea

import pytest
from pydantic import ValidationError


def test_natura_needs_to_be_set_when_aliquota_iva_is_zero():
    with pytest.raises(ValidationError) as e:
        DettaglioLinea(
            numero_linea=1,
            descrizione="Test",
            quantita="1.00",
            prezzo_unitario="1.00",
            prezzo_totale="1.00",
            aliquota_iva="0.00",
        )

    assert e.value.errors() == [
        {
            "loc": ("natura",),
            "msg": "Value error, Natura non valida per aliquota IVA 0.00: None - Test",
            "type": "value_error",
            "url": ANY,
            "ctx": ANY,
            "input": None,
        }
    ]


def test_works():
    DettaglioLinea(
        numero_linea=1,
        descrizione="Test",
        quantita="1.00",
        prezzo_unitario="1.00",
        prezzo_totale="1.00",
        aliquota_iva="0.00",
        natura="N1",
    )


def test_natura_needs_to_be_set_when_aliquota_iva_is_zero_dati_rieplilogo():
    with pytest.raises(ValidationError) as e:
        DatiRiepilogo(
            aliquota_iva="0.00",
            imponibile_importo="1.00",
            imposta="0.00",
        )

    assert e.value.errors() == [
        {
            "loc": ("natura",),
            "msg": "Value error, Natura non valida per aliquota IVA 0.00",
            "type": "value_error",
            "url": ANY,
            "ctx": ANY,
            "input": None,
        }
    ]


def test_works_dati_rieplilogo():
    DatiRiepilogo(
        aliquota_iva="0.00",
        imponibile_importo="1.00",
        imposta="0.00",
        natura="N1",
    )
