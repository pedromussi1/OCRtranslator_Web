"""Pure-function tests for ocrcore (no OCR, no model download)."""

from ocrcore.ocr import clean_text
from ocrcore.translate import detect_language, normalize_code, translate_text


def test_clean_text_dehyphenates_line_breaks():
    assert clean_text("inter-\nnational") == "international"


def test_clean_text_collapses_whitespace_and_drops_blank_lines():
    assert clean_text("  hello   world \n\n  foo  ") == "hello world\nfoo"


def test_normalize_code_maps_regional_variants():
    assert normalize_code("pt-br") == "pt"
    assert normalize_code("zh-cn") == "zh"
    assert normalize_code("EN") == "en"


def test_detect_language_english():
    assert detect_language("this is a clearly english sentence") == "en"


def test_detect_language_empty_defaults():
    assert detect_language("", default="en") == "en"


def test_translate_noop_when_same_language():
    # from == to short-circuits before any model is needed.
    assert translate_text("hello world", to_lang="en", from_lang="en") == "hello world"
