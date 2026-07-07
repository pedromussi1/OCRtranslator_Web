"""ocrcore: OCR an image and translate the text locally.

Pipeline: image -> (OpenCV preprocess) -> OCR (Tesseract) -> translate (Argos Translate).

Translation runs fully offline via Argos Translate (CTranslate2 models) — no API keys and
no per-request quota, unlike the original app's MyMemory-backed ``translate`` library.
"""

from .ocr import extract_text, clean_text
from .translate import translate_text, detect_language

__all__ = ["extract_text", "clean_text", "translate_text", "detect_language"]
