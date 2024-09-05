<h1>Explanation of the OCR Translator Code</h1>

<h2>1. Importing Libraries</h2>
<p>The code begins by importing various libraries required for the application:</p>
<pre><code>from flask import Flask, render_template, request, redirect, url_for
import cv2
import pytesseract
import os
from translate import Translator
from werkzeug.utils import secure_filename</code></pre>
<p><code>Flask</code> is used to build the web application, <code>cv2</code> (OpenCV) for image processing, <code>pytesseract</code> for OCR, <code>os</code> for file handling, <code>Translator</code> for text translation, and <code>secure_filename</code> for securing file uploads.</p>

<h2>2. Configuring Flask and Tesseract</h2>
<p>The application is configured and set up:</p>
<pre><code>app = Flask(__name__)

# Update this path to point to your Tesseract installation
pytesseract.pytesseract_cmd = '/usr/bin/tesseract'

# Directory to store uploaded and processed images
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER</code></pre>
<p><code>Flask</code> is initialized, and the path to the Tesseract executable is set. The <code>UPLOAD_FOLDER</code> directory is created to store uploaded images.</p>

<h2>3. Defining Helper Functions</h2>
<p>The code includes several helper functions:</p>
<ul>
    <li><strong>extract_text(image_path)</strong>: Reads an image, converts it to grayscale, and uses <code>pytesseract</code> to extract text.</li>
    <pre><code>def extract_text(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(gray, config=custom_config)
    return text.strip()</code></pre>

    <li><strong>preprocess_text(text)</strong>: Cleans and processes the extracted text by removing punctuation, converting to lowercase, and normalizing whitespace.</li>
    <pre><code>def preprocess_text(text):
    import re
    import string
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    text = text.lower()
    text = " ".join(text.split())
    return text</code></pre>

    <li><strong>translate_text(text, target_lang='en')</strong>: Translates the processed text into the specified language using the <code>Translator</code> class.</li>
    <pre><code>def translate_text(text, target_lang='en'):
    translator = Translator(to_lang=target_lang)
    lines = text.split('\n')
    translated_lines = []

    # To handle character limits, divide lines into manageable chunks
    for line in lines:
        chunk_size = 500
        chunks = [line[i:i + chunk_size] for i in range(0, len(line), chunk_size)]
        translated_chunks = [translator.translate(chunk) for chunk in chunks]
        translated_lines.append(''.join(translated_chunks))

    return '\n'.join(translated_lines)</code></pre>
</ul>

<h2>4. Defining the Main Route</h2>
<p>The main route handles both GET and POST requests. It processes uploaded files, extracts and translates text, and renders the result page:</p>

<pre><code>
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
</code></pre>

    
<p>This route processes uploaded files and user input, performs OCR, text preprocessing, translation, and displays the results on a web page.</p>

<h2>5. Running the Application</h2>
<p>The application is started in debug mode:</p>
<pre><code>if __name__ == "__main__":
    app.run(debug=True)</code></pre>
    
<p>This ensures the Flask application runs with debugging enabled, which is helpful during development.</p>

<h1>Explanation of HTML Templates</h1>

<h2>1. index.html</h2>
<p>This HTML file provides the interface for users to upload an image and specify the target language for translation. It is the entry point of the application where users interact with the system.</p>

<h3>Key Elements:</h3>

<ul>
    <li><strong>Form Element:</strong> 
        <p>The <code>&lt;form method="POST" enctype="multipart/form-data"&gt;</code> tag sets up a form that sends data to the server. The <code>method="POST"</code> attribute ensures that the form data is sent in the body of the HTTP request, not the URL. The <code>enctype="multipart/form-data"</code> attribute allows the form to handle file uploads.</p>
    </li>
    <li><strong>File Input:</strong> 
        <p>The <code>&lt;input type="file" name="file" accept="image/*" required&gt;</code> element lets users select an image file for upload. The <code>name="file"</code> attribute specifies the name of the file field, which is used in the backend to retrieve the uploaded file. The <code>accept="image/*"</code> attribute restricts the file types to images only, and the <code>required</code> attribute ensures that a file must be selected before submission.</p>
    </li>
    <li><strong>Target Language Input:</strong> 
        <p>The <code>&lt;input type="text" name="target_lang" placeholder="en" value="en"&gt;</code> element allows users to specify the language code for translation. The <code>name="target_lang"</code> attribute defines the name of the input field, which is used to pass the target language code to the backend. The placeholder and default value of <code>en</code> indicate that English is the default language.</p>
    </li>
    <li><strong>Submit Button:</strong> 
        <p>The <code>&lt;button type="submit"&gt;</code> element submits the form data to the server. When clicked, it triggers the form submission, which sends the selected image file and target language to the backend for processing.</p>
    </li>
    <li><strong>Language Cheat Sheet:</strong> 
        <p>The <code>&lt;div class="language-cheat-sheet"&gt;</code> provides a reference for users to know the language codes they can use for translation. This section is useful for users to select the correct language code and understand what options are available.</p>
        <ul>
            <li><strong>Language Codes:</strong> 
                <p>The <code>&lt;ul&gt;</code> element lists various language codes and their corresponding languages, such as <code>en</code> for English and <code>es</code> for Spanish. This helps users ensure they use the correct code for their desired translation language.</p>
            </li>
        </ul>
    </li>
</ul>

<h2>2. result.html</h2>
<p>This HTML file is used to display the results after the image has been processed. It shows the original image, the recognized text, and the translated text. This page is rendered after the backend processes the uploaded image and performs translation.</p>

<h3>Key Elements:</h3>

<ul>
    <li><strong>Original Image:</strong> 
        <p>The <code>&lt;img src="{{ url_for('static', filename='uploads/' + original_image) }}" alt="Original Image"&gt;</code> tag displays the uploaded image. The <code>src</code> attribute uses the <code>url_for('static', filename='uploads/' + original_image)</code> function to generate the correct URL for the image file stored in the <code>static/uploads</code> directory. This allows the image to be displayed on the results page.</p>
    </li>
    <li><strong>Recognized Text:</strong> 
        <p>The <code>&lt;pre&gt;</code> tag is used to display the extracted text from the image in a preformatted manner, preserving whitespace and formatting. This ensures that the text appears as it was recognized from the image.</p>
    </li>
    <li><strong>Translated Text:</strong> 
        <p>The <code>&lt;pre&gt;</code> tag also displays the translated text, maintaining the same formatting as the recognized text. This section shows the output of the translation process, allowing users to see the result of their selected target language.</p>
    </li>
    <li><strong>Link to Upload Another Image:</strong> 
        <p>The <code>&lt;a href="{{ url_for('index') }}"&gt;</code> tag provides a hyperlink to return to the upload form. This link allows users to upload another image without having to manually navigate back to the starting page.</p>
    </li>
</ul>


