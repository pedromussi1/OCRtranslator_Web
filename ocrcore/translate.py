"""Local, offline translation via Argos Translate (CTranslate2 models).

Replaces the original app's ``translate`` library (which called the MyMemory web API and
was subject to a daily character quota). Language packages are downloaded once on first use
and then cached under the Argos data dir; subsequent translations are fully offline.
"""

from __future__ import annotations

import threading

from langdetect import detect

_install_lock = threading.Lock()
_installed_pairs: set[tuple[str, str]] = set()

# Map common regional/UI codes (from the language cheat sheet and langdetect) to the
# ISO 639-1 codes Argos Translate uses.
_CODE_ALIASES = {"pt-br": "pt", "zh-cn": "zh", "zh-tw": "zh"}


def normalize_code(code: str) -> str:
    """Normalize a language code to the form Argos Translate expects (e.g. pt-br -> pt)."""
    code = code.strip().lower()
    if code in _CODE_ALIASES:
        return _CODE_ALIASES[code]
    return code.split("-")[0]  # drop any region subtag


def detect_language(text: str, default: str = "en") -> str:
    """Best-effort source-language code (ISO 639-1) from the OCR text."""
    text = text.strip()
    if not text:
        return default
    try:
        return normalize_code(detect(text))
    except Exception:
        return default


def _install_one(from_code: str, to_code: str, available) -> bool:
    """Install a single direct Argos package if available. Returns True on success."""
    import argostranslate.package

    match = next(
        (p for p in available if p.from_code == from_code and p.to_code == to_code), None
    )
    if match is None:
        return False
    argostranslate.package.install_from_path(match.download())
    return True


def _ensure_package(from_code: str, to_code: str) -> None:
    """Ensure a translation path exists for ``from_code -> to_code``.

    Installs the direct package when available; otherwise falls back to an English pivot
    (``from -> en`` + ``en -> to``), which Argos chains automatically. Raises ValueError
    if no path can be built.
    """
    key = (from_code, to_code)
    if key in _installed_pairs:
        return
    import argostranslate.package
    import argostranslate.translate

    with _install_lock:
        if key in _installed_pairs:
            return
        installed = {
            (lang.code, t.to_lang.code)
            for lang in argostranslate.translate.get_installed_languages()
            for t in lang.translations_from
        }
        if key not in installed:
            argostranslate.package.update_package_index()
            available = argostranslate.package.get_available_packages()
            if not _install_one(from_code, to_code, available):
                # No direct model — pivot through English.
                ok_from = from_code == "en" or _install_one(from_code, "en", available)
                ok_to = to_code == "en" or _install_one("en", to_code, available)
                if not (ok_from and ok_to):
                    raise ValueError(
                        f"No Argos Translate path available for {from_code} -> {to_code}."
                    )
        _installed_pairs.add(key)


def translate_text(text: str, to_lang: str = "en", from_lang: str | None = None) -> str:
    """Translate ``text`` into ``to_lang``. Detects the source language if not given.

    Returns the input unchanged when source and target languages match.
    """
    if not text.strip():
        return text
    to_lang = normalize_code(to_lang)
    from_lang = normalize_code(from_lang) if from_lang else detect_language(text)
    if from_lang == to_lang:
        return text

    import argostranslate.translate

    _ensure_package(from_lang, to_lang)
    return argostranslate.translate.translate(text, from_lang, to_lang)
