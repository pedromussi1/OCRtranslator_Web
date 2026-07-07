# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-07-07

### Added
- Redesigned web UI matching the OCR BookFinder design system: responsive, dark-mode-aware
  layout with a shared base template, drag-and-drop upload + image preview, a language
  dropdown, a loading state during translation, and a cleaner results page that shows the
  translation prominently with the detected `source → target` languages.

### Changed
- The result page now displays the auto-detected source language alongside the target.

## [2.0.0] - 2026-07-06

Complete rewrite: self-contained, offline translation with an honest README.

### Added
- `ocrcore/` pipeline: preprocess (OpenCV) → OCR (Tesseract) → detect language → translate.
- **Argos Translate** local, offline neural machine translation — no API key, no quota.
- Automatic source-language detection (`langdetect`) and regional-code normalization
  (e.g. `pt-br` → `pt`).
- English-pivot fallback for language pairs without a direct model.
- Configurable OpenCV preprocessing (upscale, denoise, Otsu threshold, deskew).
- `pytest` suite, pinned `requirements.txt`.

### Fixed
- **False README claim**: described the "Azure Translation API"; the code actually used the
  `translate` library's free MyMemory web API (daily quota). Replaced with local Argos Translate.
- **Tesseract typo**: `pytesseract.pytesseract_cmd` set the wrong attribute (a silent no-op)
  and was Linux-only → cross-platform discovery.
- `debug=True` in production; added upload type/size validation and unique filenames.

### Changed
- Docker image now serves via **gunicorn** instead of the Flask dev server.
- README rewritten to describe the real (local, offline) stack.

### Removed
- The `translate` / MyMemory dependency.
- Duplicated `MC_ocr_translation.py` (logic now lives in `ocrcore/`).
- Runtime upload artifacts from version control.

[2.1.0]: https://github.com/pedromussi1/OCRtranslator_Web/releases/tag/v2.1.0
[2.0.0]: https://github.com/pedromussi1/OCRtranslator_Web/releases/tag/v2.0.0
