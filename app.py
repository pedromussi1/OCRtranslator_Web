from flask import Flask, render_template, request, redirect, url_for
import cv2
import pytesseract
import os
from translate import Translator
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Update this path to point to your Tesseract installation
pytesseract.pytesseract_cmd = '/usr/bin/tesseract'

# Directory to store uploaded and processed images
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_text(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(gray, config=custom_config)
    return text.strip()

def preprocess_text(text):
    import re
    import string
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    text = text.lower()
    text = " ".join(text.split())
    return text

def translate_text(text, target_lang='en'):
    translator = Translator(to_lang=target_lang)
    lines = text.split('\n')
    translated_lines = []

    # To handle character limits, divide lines into manageable chunks
    for line in lines:
        chunk_size = 500
        chunks = [line[i:i + chunk_size] for i in range(0, len(line), chunk_size)]
        translated_chunks = [translator.translate(chunk) for chunk in chunks]
        translated_lines.append(''.join(translated_chunks))

    return '\n'.join(translated_lines)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        target_lang = request.form.get('target_lang', 'en')

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Extract and preprocess text using the same method as your other app
            text = extract_text(file_path)
            processed_text = preprocess_text(text)
            translated_text = translate_text(processed_text, target_lang)

            return render_template(
                'result.html',
                original_image=filename,
                text=text,
                translated_text=translated_text
            )

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
