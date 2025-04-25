from __future__ import annotations

import unidecode


def normalize_unicode(value: str) -> str:
    return unidecode.unidecode(value).encode("latin_1")
