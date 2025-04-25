from __future__ import annotations
from collections import defaultdict

from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pretix_fattura_elettronica.models import InvoiceLog
from pretix_fattura_elettronica.utils import get_codice_fiscale, get_pec, get_sdi
from pretix_fattura_elettronica.utils.normalise_unicode import normalize_unicode

from django.db.models import Count

from pretix.base.models import Invoice, Order
from pydantic import BaseModel, Field, model_validator, validator
from pydantic.functional_serializers import field_serializer

from .enums import DOC_TYPE as DT
from .enums import SETTINGS
from .utils.tax import get_tax_category


class DettaglioLinea(BaseModel):
    numero_linea: Annotated[int, Field(serialization_alias="NumeroLinea")]
    descrizione: Annotated[str, Field(serialization_alias="Descrizione")]
    quantita: Annotated[str | None, Field(serialization_alias="Quantita")] = None
    unita_misura: Annotated[str | None, Field(serialization_alias="UnitaMisura")] = None
    prezzo_unitario: Annotated[str, Field(serialization_alias="PrezzoUnitario")]
    prezzo_totale: Annotated[str, Field(serialization_alias="PrezzoTotale")]
    aliquota_iva: Annotated[str, Field(serialization_alias="AliquotaIVA")]
    ritenuta: Annotated[str | None, Field(serialization_alias="Ritenuta")] = None
    natura: Annotated[str | None, Field(serialization_alias="Natura")] = None

    # validate natura based on aliquota_iva
    @validator("natura", always=True)
    def check_natura(cls, v: str | None, values: dict[str, str | None]) -> str | None:
        description = values.get("descrizione")
        if values.get("aliquota_iva") == "0.00" and not v:
            raise ValueError(
                f"Natura non valida per aliquota IVA 0.00: {v} - {description}"
            )

        return v


class DatiRiepilogo(BaseModel):
    aliquota_iva: Annotated[str, Field(serialization_alias="AliquotaIVA")]
    natura: Annotated[str | None, Field(serialization_alias="Natura")] = None
    imponibile_importo: Annotated[str, Field(serialization_alias="ImponibileImporto")]
    imposta: Annotated[str, Field(serialization_alias="Imposta")]

    @validator("natura", always=True)
    def check_natura(cls, v: str | None, values: dict[str, str | None]) -> str | None:
        if values.get("aliquota_iva") == "0.00" and not v:
            raise ValueError("Natura non valida per aliquota IVA 0.00")

        return v


class DatiBeniServizi(BaseModel):
    dettaglio_linee: Annotated[
        list[DettaglioLinea], Field(serialization_alias="DettaglioLinee")
    ]

    # DatiRiepilogo (blocco obbligtorio che può ripetersi più volte per ogni
    # fattura fino a un massimo di 1000 occorrenze. Ogni ripetizione conterrà le
    # informazioni aggregate per ciascun valore di aliquota IVA applicata alle
    # operazioni elencate nel documento e, nel caso di imposta a zero, per
    # ciascun motivo di esclusione, come riportato nell'elemento Natura.
    # Inoltre, per la stessa aliquota IVA o per la stessa natura, può ripetersi per
    # differenziare i valori riferiti a spese detraibili o deducibili da quelli riferiti a
    # spese non detraibili né deducibili).
    dati_riepilogo: Annotated[
        list[DatiRiepilogo], Field(serialization_alias="DatiRiepilogo")
    ]


class DettaglioPagamento(BaseModel):
    modalita_pagamento: Annotated[str, Field(serialization_alias="ModalitaPagamento")]
    importo_pagamento: Annotated[str, Field(serialization_alias="ImportoPagamento")]


class DatiPagamento(BaseModel):
    condizioni_pagamento: Annotated[
        str | None, Field(serialization_alias="CondizioniPagamento")
    ] = None
    dettaglio_pagamento: Annotated[
        DettaglioPagamento, Field(serialization_alias="DettaglioPagamento")
    ]


class IdFiscaleIVA(BaseModel):
    id_paese: Annotated[
        str, Field(serialization_alias="IdPaese", min_length=2, max_length=2)
    ]
    id_codice: Annotated[
        str, Field(serialization_alias="IdCodice", min_length=1, max_length=28)
    ]


class Anagrafica(BaseModel):
    """Denominazione or Nome and Cognome should be filled"""

    denominazione: Annotated[str | None, Field(serialization_alias="Denominazione")] = (
        None
    )
    nome: Annotated[str | None, Field(serialization_alias="Nome")] = None
    cognome: Annotated[str | None, Field(serialization_alias="Cognome")] = None
    titolo: Annotated[str | None, Field(serialization_alias="Titolo")] = None
    cod_eori: Annotated[str | None, Field(serialization_alias="CodEORI")] = None

    @model_validator(mode="after")
    def check_valid_data(self) -> Anagrafica:
        if self.denominazione is None:
            if self.cognome is None and self.nome is None:
                raise ValueError(
                    "Necessaria denominazione oppure nome e cognome del destinatario."
                )
            if self.cognome is None or self.nome is None:
                raise ValueError(
                    "In mancanza di Ragione Sociale, nome e cognome non possono essere vuoti."
                )
        return self


class DatiAnagraficiCedente(BaseModel):
    id_fiscale_iva: Annotated[IdFiscaleIVA, Field(serialization_alias="IdFiscaleIVA")]
    codice_fiscale: Annotated[str | None, Field(serialization_alias="CodiceFiscale")]
    anagrafica: Annotated[Anagrafica, Field(serialization_alias="Anagrafica")]
    regime_fiscale: Annotated[str, Field(serialization_alias="RegimeFiscale")]

    @field_serializer("codice_fiscale")
    def serialize_codice_fiscale(self, codice_fiscale: str | None):
        if codice_fiscale is None:
            return None

        return codice_fiscale.upper()


class DatiAnagraficiCessionario(BaseModel):
    id_fiscale_iva: Annotated[
        IdFiscaleIVA | None, Field(serialization_alias="IdFiscaleIVA")
    ]
    codice_fiscale: Annotated[str | None, Field(serialization_alias="CodiceFiscale")]
    anagrafica: Annotated[Anagrafica, Field(serialization_alias="Anagrafica")]

    @field_serializer("codice_fiscale")
    def serialize_codice_fiscale(self, codice_fiscale: str | None):
        if codice_fiscale is None:
            return None

        return codice_fiscale.upper()


class Sede(BaseModel):
    indirizzo: Annotated[str, Field(serialization_alias="Indirizzo", min_length=2)]
    numero_civico: Annotated[str | None, Field(serialization_alias="NumeroCivico")] = (
        None
    )
    cap: Annotated[str, Field(serialization_alias="CAP")]
    comune: Annotated[str, Field(serialization_alias="Comune", min_length=2)]
    provincia: Annotated[str | None, Field(serialization_alias="Provincia")] = None
    nazione: Annotated[
        str, Field(serialization_alias="Nazione", min_length=2, max_length=2)
    ]

    @field_serializer("cap")
    def serialize_cap(self, cap: str):
        if self.nazione == "IT":
            return cap

        return "00000"

    @field_serializer("indirizzo")
    def serialize_indirizzo(self, indirizzo: str):
        return normalize_unicode(indirizzo).decode()[:60]


class Contatti(BaseModel):
    telefono: Annotated[str | None, Field(serialization_alias="Telefono")] = None
    fax: Annotated[str | None, Field(serialization_alias="Fax")] = None
    email: Annotated[str | None, Field(serialization_alias="Email")] = None


class DatiTrasmissione(BaseModel):
    id_trasmittente: Annotated[
        IdFiscaleIVA | None, Field(serialization_alias="IdTrasmittente")
    ] = None
    progressivo_invio: Annotated[
        str | None, Field(serialization_alias="ProgressivoInvio")
    ] = None
    formato_trasmissione: Annotated[
        str, Field(serialization_alias="FormatoTrasmissione")
    ] = "FPR12"
    codice_destinatario: Annotated[str, Field(serialization_alias="CodiceDestinatario")]
    pec_destinatario: Annotated[
        str | None, Field(serialization_alias="PECDestinatario")
    ] = None

    @field_serializer("progressivo_invio")
    def serialize_progressivo_invio(self, progressivo_invio: str):
        return progressivo_invio.replace("TEST", "")


class CedentePrestatore(BaseModel):
    dati_anagrafici: Annotated[
        DatiAnagraficiCedente, Field(serialization_alias="DatiAnagrafici")
    ]
    sede: Annotated[Sede, Field(serialization_alias="Sede")]
    contatti: Annotated[Contatti | None, Field(serialization_alias="Contatti")] = None


class CessionarioCommittente(BaseModel):
    dati_anagrafici: Annotated[
        DatiAnagraficiCessionario, Field(serialization_alias="DatiAnagrafici")
    ]
    sede: Annotated[Sede, Field(serialization_alias="Sede")]


class DatiGeneraliDocumento(BaseModel):
    tipo_documento: Annotated[str, Field(serialization_alias="TipoDocumento")]
    divisa: Annotated[str, Field(serialization_alias="Divisa")]
    data: Annotated[datetime, Field(serialization_alias="Data")]
    numero: Annotated[str, Field(serialization_alias="Numero")]

    @field_serializer("data")
    def serialize_data(self, data: datetime):
        return data.date().strftime("%Y-%m-%d")


class DatiGenerali(BaseModel):
    dati_generali_documento: Annotated[
        DatiGeneraliDocumento, Field(serialization_alias="DatiGeneraliDocumento")
    ]


class FatturaElettronicaBody(BaseModel):
    dati_generali: Annotated[DatiGenerali, Field(serialization_alias="DatiGenerali")]
    dati_beni_servizi: Annotated[
        DatiBeniServizi, Field(serialization_alias="DatiBeniServizi")
    ]
    dati_pagamento: Annotated[DatiPagamento, Field(serialization_alias="DatiPagamento")]


class FatturaElettronicaHeader(BaseModel):
    dati_trasmissione: Annotated[
        DatiTrasmissione, Field(serialization_alias="DatiTrasmissione")
    ]
    cedente_prestatore: Annotated[
        CedentePrestatore, Field(serialization_alias="CedentePrestatore")
    ]
    cessionario_committente: Annotated[
        CessionarioCommittente, Field(serialization_alias="CessionarioCommittente")
    ]


class FatturaElettronica(BaseModel):
    fattura_elettronica_header: Annotated[
        FatturaElettronicaHeader, Field(serialization_alias="FatturaElettronicaHeader")
    ]
    fattura_elettronica_body: Annotated[
        list[FatturaElettronicaBody],
        Field(serialization_alias="FatturaElettronicaBody"),
    ]


class OrderSerializer:
    def __init__(self, order: Order) -> None:
        self._order = order

    @classmethod
    def serialize_invoices(
        cls, order: Order
    ) -> list[tuple[Invoice, FatturaElettronica]]:
        return cls(order)._serialize_invoices()

    def _serialize_invoices(self) -> list[tuple[Invoice, FatturaElettronica]]:
        return [
            (invoice, InvoiceSerializer.serialize(invoice))
            for invoice in self._invoices
            if invoice not in self._invoice_already_sent
        ]

    @property
    def _invoices(self) -> list[Invoice]:
        return self._order.invoices.all()

    @property
    def _invoice_already_sent(self) -> set[Invoice]:
        already_sent = InvoiceLog.objects.filter(uuid__isnull=False)
        return set([inv.invoice for inv in already_sent])


class InvoiceSerializer:
    def __init__(self, invoice: Invoice) -> None:
        self._invoice = invoice

    @classmethod
    def serialize(cls, invoice: Invoice) -> FatturaElettronica:
        return cls(invoice)._serialize()

    def _serialize(self) -> FatturaElettronica:
        return FatturaElettronica(
            fattura_elettronica_header=self._invoice_header,
            fattura_elettronica_body=[self._invoice_body],
        )

    @property
    def _invoice_body(self) -> FatturaElettronicaBody:
        inv = self._invoice
        tipo_doc = DT.TD04 if inv.canceled and inv.is_cancellation else DT.TD01
        dati_generali = DatiGenerali(
            dati_generali_documento=DatiGeneraliDocumento(
                tipo_documento=tipo_doc,
                divisa=inv.event.currency,
                data=inv.date,
                numero=inv.number,
            )
        )
        lines = inv.lines.all()

        dettaglio_linee = [
            DettaglioLinea(
                numero_linea=i + 1,
                descrizione=line.description,
                prezzo_unitario=str(line.net_value),
                prezzo_totale=str(line.net_value),
                aliquota_iva=str(line.tax_rate),
                quantita="1.00",
                natura=get_tax_category(line),
            )
            for i, line in enumerate(lines)
        ]

        lines_by_category_and_rate = defaultdict(list)

        for line in lines:
            category = get_tax_category(line)
            rate = line.tax_rate

            lines_by_category_and_rate[category, rate].append(line)

        dati_riepilogo = []

        for (category, tax_rate), cat_lines in lines_by_category_and_rate.items():
            imponibile_importo = sum(line.net_value for line in cat_lines)

            imposta = Decimal(tax_rate) * imponibile_importo / 100

            dati_riepilogo.append(
                DatiRiepilogo(
                    aliquota_iva=f"{tax_rate:.2f}",
                    imponibile_importo=f"{imponibile_importo:.2f}",
                    imposta=f"{imposta:.2f}",
                    natura=category,
                )
            )

        dati_beni_servizi = DatiBeniServizi(
            dettaglio_linee=dettaglio_linee, dati_riepilogo=dati_riepilogo
        )

        total_invoice = sum([line.gross_value for line in lines])

        last_payment = inv.order.payments.last()
        payment_provider = last_payment.provider

        payment_method = "MP05" if payment_provider == "banktransfer" else "MP08"

        dati_pagamento = DatiPagamento(
            condizioni_pagamento="TP02",
            dettaglio_pagamento=DettaglioPagamento(
                modalita_pagamento=payment_method,
                importo_pagamento=f"{total_invoice:.2f}",
            ),
        )
        return FatturaElettronicaBody(
            dati_generali=dati_generali,
            dati_beni_servizi=dati_beni_servizi,
            dati_pagamento=dati_pagamento,
        )

    @property
    def _invoice_header(self) -> FatturaElettronicaHeader:
        inv = self._invoice

        dati_trasmissione = DatiTrasmissione(
            id_trasmittente=IdFiscaleIVA(
                id_paese=inv.invoice_from_country.code,
                id_codice=inv.invoice_from_vat_id,
            ),
            codice_destinatario=self.codice_destinatario,
            pec_destinatario=self.pec,
            progressivo_invio=inv.number,
        )
        # Cedente Prestatore is who issue the invoice: e.g. Python Italia APS
        cedente_prestatore = CedentePrestatore(
            dati_anagrafici=DatiAnagraficiCedente(
                id_fiscale_iva=IdFiscaleIVA(
                    id_paese=inv.invoice_from_country.code,
                    id_codice=inv.invoice_from_vat_id,
                ),
                codice_fiscale=SETTINGS.CF,
                anagrafica=Anagrafica(denominazione=inv.invoice_from_name),
                regime_fiscale=SETTINGS.REGIME_FISCALE,
            ),
            sede=Sede(
                indirizzo=inv.invoice_from,
                numero_civico=None,
                cap=inv.invoice_from_zipcode,
                comune=inv.invoice_from_city,
                provincia=None,
                nazione=inv.invoice_from_country.code,
            ),
            contatti=Contatti(email=SETTINGS.EMAIL),
        )

        if self.vat_id or not self.is_italian_invoice:
            id_fiscale_iva = IdFiscaleIVA(
                id_paese=inv.invoice_to_country.code,
                id_codice=self.vat_id or "99999999999",
            )
        else:
            id_fiscale_iva = None

        cessionario_committente = CessionarioCommittente(
            dati_anagrafici=DatiAnagraficiCessionario(
                id_fiscale_iva=id_fiscale_iva,
                codice_fiscale=self.codice_fiscale,
                anagrafica=self._recipient_registry_data,
            ),
            sede=Sede(
                indirizzo=inv.invoice_to,
                numero_civico=None,
                cap=inv.invoice_to_zipcode,
                comune=inv.invoice_to_city,
                provincia=None,
                nazione=inv.invoice_to_country.code,
            ),
        )
        return FatturaElettronicaHeader(
            dati_trasmissione=dati_trasmissione,
            cedente_prestatore=cedente_prestatore,
            cessionario_committente=cessionario_committente,
        )

    @property
    def _recipient_registry_data(self) -> Anagrafica:
        inv = self._invoice
        complete_name = inv.order.invoice_address.name
        family_name = complete_name.rsplit(" ", 1)[-1] if complete_name else None
        name = (
            complete_name.rsplit(" ", 1)[0]
            if complete_name and " " in complete_name
            else None
        )

        # in the XML we can have both Denominazione and (Nome and Cognome)

        if inv.invoice_to_company:
            return Anagrafica(
                denominazione=inv.invoice_to_company,
            )

        return Anagrafica(
            nome=name,
            cognome=family_name,
        )

    @property
    def is_italian_invoice(self) -> bool:
        return self._invoice.invoice_to_country.code == "IT"

    @property
    def is_business_invoice(self) -> bool:
        return self._invoice.order.invoice_address.is_business

    @property
    def codice_destinatario(self) -> str:
        invoice = self._invoice

        codice_destinatario = get_sdi(invoice.order)

        if self.is_italian_invoice:
            if self.is_business_invoice and not codice_destinatario:
                return "0000000"
        else:
            return "XXXXXXX"

        return codice_destinatario or SETTINGS.CODICE_DESTINATARIO_DEFAULT

    @property
    def pec(self) -> str | None:
        return get_pec(self._invoice.order)

    @property
    def vat_id(self) -> str | None:
        if self.is_business_invoice:
            return self._invoice.invoice_to_vat_id

        return None

    @property
    def codice_fiscale(self) -> str | None:
        codice_fiscale = get_codice_fiscale(self._invoice.order)

        if self.is_italian_invoice:
            if not self.is_business_invoice and not codice_fiscale:
                raise ValueError("Codice fiscale is required.")

        return codice_fiscale
