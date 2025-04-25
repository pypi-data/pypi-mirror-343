from __future__ import annotations

import io
import zipfile
from datetime import datetime
from decimal import Decimal
from typing import Any

from pretix_fattura_elettronica.utils.normalise_unicode import normalize_unicode
import unidecode
from lxml import etree
from pretix.base.models import Invoice, Order

EtreeElement = etree._Element  # type: ignore


def _get_order_meta(order: Order) -> dict[str, Any]:
    return order.meta_info_data  # type: ignore


def get_codice_fiscale(order: Order) -> str | None:
    data = _get_order_meta(order)

    return data.get("codice_fiscale") or data.get("contact_form_data", {}).get(
        "codice_fiscale"
    )


def get_pec(order: Order) -> str | None:
    data = _get_order_meta(order)

    return data.get("pec") or data.get("contact_form_data", {}).get("pec")


def get_sdi(order: Order) -> str | None:
    data = _get_order_meta(order)

    return data.get("sdi") or data.get("contact_form_data", {}).get("sdi")


def _split_tags(tag_name: str, text: bytes) -> list[EtreeElement]:
    tags: list[EtreeElement] = []

    size = 200

    chunks = [text[y - size : y] for y in range(size, len(text) + size, size)]

    for value in chunks:
        tag = etree.Element(tag_name)
        tag.text = value
        tags.append(tag)

    return tags


# TODO: maybe make this recursive?
XMLDict = dict[str, str | int | list[Any] | Any]


# TODO: maybe use pydantic xml
def dict_to_xml(data: XMLDict):
    tags: list[EtreeElement] = []

    for key, value in data.items():
        # skip empty value

        if not value:
            continue

        if isinstance(value, (dict, list)):
            if not isinstance(value, list):
                value = [value]

            for item in value:
                tag = etree.Element(key)

                for subtag in dict_to_xml(item):
                    tag.append(subtag)

                tags.append(tag)
        else:
            if isinstance(value, (int, float, Decimal)):
                value = str(value)

            if isinstance(value, datetime):
                value = value.isoformat()

            value = normalize_unicode(value)

            for tag in _split_tags(key, value):
                tags.append(tag)

    return tags


def create_zip_file(files: dict[str, str]) -> bytes:
    in_memory_zip = io.BytesIO()

    with zipfile.ZipFile(in_memory_zip, "w") as zip_file:
        for filename, content in files.items():
            zip_file.writestr(filename, content)

    return in_memory_zip.getvalue()


def invoice_to_xml(invoice: Invoice) -> str:
    from pretix_fattura_elettronica.serializers import InvoiceSerializer

    invoice_data = InvoiceSerializer.serialize(invoice).model_dump(by_alias=True)

    NAMESPACE_MAP = {
        "p": "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2",
        "ds": "http://www.w3.org/2000/09/xmldsig#",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }

    SCHEMA_LOCATION = (
        "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2 "
        "http://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2"
        "/Schema_del_file_xml_FatturaPA_versione_1.2.xsd"
    )

    root_tag = "{%s}FatturaElettronica" % NAMESPACE_MAP["p"]
    schema_location_key = "{%s}schemaLocation" % NAMESPACE_MAP["xsi"]

    root = etree.Element(
        root_tag,
        attrib={schema_location_key: SCHEMA_LOCATION},
        nsmap=NAMESPACE_MAP,
        versione="FPR12",
    )

    tags = dict_to_xml(invoice_data)

    for tag in tags:
        root.append(tag)

    return etree.tostring(root, pretty_print=True)
