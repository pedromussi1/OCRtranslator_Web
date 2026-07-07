"""OCR: image path -> text, with optional OpenCV preprocessing.

Unlike the book-finder's query normalizer (which strips punctuation for search), this keeps
punctuation and case so the translation stays readable — it only rejoins words hyphenated
across line breaks.
"""

from __future__ import annotations

import re

import cv2
import pytesseract

from .preprocess import PreprocessConfig, preprocess
from .tesseract_setup import configure_tesseract

configure_tesseract()

_OCR_CONFIG = r"--oem 3 --psm 6"


def extract_text(image_path: str, preprocess_config: PreprocessConfig | None = None) -> str:
    """Read text from an image file. ``preprocess_config`` controls the OpenCV pipeline."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")
    processed = preprocess(image, preprocess_config)
    text = pytesseract.image_to_string(processed, config=_OCR_CONFIG)
    return clean_text(text.strip())


def clean_text(text: str) -> str:
    """Rejoin words split by a hyphen at a line break; collapse trailing whitespace."""
    text = re.sub(r"-\s*\n\s*", "", text)     # de-hyphenate across line breaks
    lines = [" ".join(line.split()) for line in text.splitlines()]
    return "\n".join(line for line in lines if line)
