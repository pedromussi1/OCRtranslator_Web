"""Flask app: upload an image, OCR the text, and translate it locally.

Rewritten to use the ``ocrcore`` pipeline. Translation now runs offline via Argos Translate
instead of the original MyMemory-backed ``translate`` library (which had a daily quota, and
which the old README incorrectly described as the "Azure Translation API").

Also fixes: the no-op ``pytesseract.pytesseract_cmd`` typo (now handled by cross-platform
Tesseract discovery), ``debug=True`` in production, missing upload validation, and
colliding upload filenames.
"""

import os
import uuid

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from ocrcore import detect_language, extract_text, translate_text

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB cap

# Language code -> display name, for a friendly "Spanish → English" label on the result.
LANGUAGES = {
    "ar": "Arabic", "de": "German", "en": "English", "es": "Spanish", "fr": "French",
    "hi": "Hindi", "it": "Italian", "ja": "Japanese", "ko": "Korean", "nl": "Dutch",
    "pl": "Polish", "pt": "Portuguese", "ru": "Russian", "tr": "Turkish", "uk": "Ukrainian",
    "zh": "Chinese",
}


def _lang_name(code: str) -> str:
    return LANGUAGES.get(code, code.upper())


def _allowed(filename: str) -> bool:
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        target_lang = request.form.get("target_lang", "en")

        if not file or not file.filename:
            return render_template("index.html", error="Please choose an image to upload.")
        if not _allowed(file.filename):
            return render_template("index.html", error="Unsupported file type.")

        ext = os.path.splitext(secure_filename(file.filename))[1].lower()
        stored_name = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], stored_name)
        file.save(file_path)

        text = extract_text(file_path)
        source_lang = detect_language(text)
        try:
            translated_text = translate_text(text, to_lang=target_lang, from_lang=source_lang)
        except ValueError as exc:
            # e.g. no Argos package for the requested language pair
            return render_template("index.html", error=str(exc))

        return render_template(
            "result.html",
            original_image=stored_name,
            text=text,
            translated_text=translated_text,
            source_name=_lang_name(source_lang),
            target_name=_lang_name(target_lang),
        )

    return render_template("index.html")


if __name__ == "__main__":
    # debug OFF by default; enable with FLASK_DEBUG=1 for local dev only.
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
