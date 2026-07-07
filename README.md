<h1 align="center">OCR Translator Web</h1>

<p align="center">
  <a href="https://youtu.be/nas4T9-hjTs"><img src="https://i.imgur.com/KCK0WYy.gif" alt="YouTube Demonstration" width="800"></a>
</p>

<p align="center">Upload an image; the app OCRs the text and translates it into your chosen language — <b>fully offline</b>, no API keys or quotas.</p>

<p align="center"><b>🚀 Live demo:</b> <a href="https://huggingface.co/spaces/Zao0531/ocr-translator">huggingface.co/spaces/Zao0531/ocr-translator</a></p>

## What changed from the original

The original app worked but had one misleading claim and several rough edges. This rewrite
makes it honest and self-contained:

| Original | Now |
|---|---|
| README claimed the **Azure Translation API**; the code actually called the `translate` library's free **MyMemory** web API (daily character quota) | **Argos Translate** — local, offline neural MT (CTranslate2). No API key, no quota, works with no internet after the model downloads once |
| Fixed target language, no source detection | Automatic source-language detection (`langdetect`) + regional-code normalization (`pt-br` → `pt`) |
| `pytesseract.pytesseract_cmd = '/usr/bin/tesseract'` — a **typo** (wrong attribute; a silent no-op) and Linux-only | Cross-platform Tesseract discovery (PATH → known dirs → `TESSERACT_CMD`) |
| Grayscale-only preprocessing | Configurable OpenCV pipeline (upscale, denoise, Otsu threshold, deskew) |
| `debug=True`, no upload validation, `flask run` in Docker | Debug off by default, file-type/size checks, unique filenames, **gunicorn** in Docker |
| No tests, unpinned deps, `translate` dependency | `pytest` suite, pinned `requirements.txt` |

## How it works

```
image ──▶ preprocess (OpenCV) ──▶ OCR (Tesseract) ──▶ detect language ──▶ translate (Argos) ──▶ text
```

Everything lives in [`ocrcore/`](ocrcore/); `app.py` is a thin Flask layer on top.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate            # (source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
python app.py                     # http://127.0.0.1:5000/
```

Tesseract must be installed separately (`winget install tesseract`,
`brew install tesseract`, `apt install tesseract-ocr`). Argos downloads the requested
language model automatically on first use, then runs offline.

## Docker

```bash
docker build -t ocr-translator .
docker run -p 5000:5000 -v argos-models:/app/.argos ocr-translator
```

The volume persists downloaded translation models across restarts.

## Notes

- OCR defaults to **English source text**. To OCR other scripts, install the matching
  Tesseract language data (e.g. `tesseract-ocr-por`) — translation of the *result* is
  already handled by Argos.
- Not every language pair has a direct Argos model; some route through English as a pivot.

## Tests

```bash
python -m pytest -q
```
