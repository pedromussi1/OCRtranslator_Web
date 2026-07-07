# Code Breakdown

OCR Translator reads text from an image and translates it — **fully offline**. The logic
lives in the `ocrcore/` package; `app.py` is a thin Flask layer.

## Pipeline

```
image ─▶ preprocess (OpenCV) ─▶ OCR (Tesseract) ─▶ detect language ─▶ translate (Argos)
```

## `ocrcore/preprocess.py`
A configurable OpenCV pipeline (upscale → denoise → Otsu threshold → deskew) to clean the
image before OCR.

## `ocrcore/ocr.py`
Runs Tesseract (`--oem 3 --psm 6`) on the preprocessed image. Tesseract is located
cross-platform (PATH → common install dirs → `TESSERACT_CMD`), fixing the original no-op
`pytesseract.pytesseract_cmd` typo. The OCR text is cleaned (hyphenated line breaks rejoined)
while keeping punctuation and case so the translation stays readable.

## `ocrcore/translate.py`
Translation via **Argos Translate** (local, offline neural MT) — replacing the original
`translate`/MyMemory web API (which had a daily quota, and which the old README wrongly
called "Azure Translation API"). It:
- auto-detects the source language (`langdetect`) and normalizes codes (e.g. `pt-br` → `pt`),
- downloads the needed language package once, then runs offline,
- falls back to an **English pivot** when a language pair has no direct model.

## `app.py`
Validates the upload, runs `extract_text` → `translate_text`, and renders the translation
with the detected source → target languages. Debug is off by default, uploads are validated
and given unique names, and the Docker image serves via gunicorn.
