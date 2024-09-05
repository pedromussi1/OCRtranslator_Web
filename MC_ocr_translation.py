import cv2
import pytesseract
from translate import Translator

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def detect_text(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform OCR using Tesseract
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(gray, config=custom_config)

    return text.strip()


def preprocess_text(text):
    # Join hyphenated words split across lines
    lines = text.split('\n')
    processed_lines = []
    skip_next = False

    for i in range(len(lines)):
        if skip_next:
            skip_next = False
            continue

        if lines[i].endswith('-') and i < len(lines) - 1:
            # Remove hyphen and join with next line
            processed_lines.append(lines[i][:-1] + lines[i + 1])
            skip_next = True
        else:
            processed_lines.append(lines[i])

    return '\n'.join(processed_lines)


def translate_text(text, target_lang='en'):
    # Translate text line by line
    translator = Translator(to_lang=target_lang)

    lines = text.split('\n')
    translated_lines = []

    for line in lines:
        # Split the line into chunks of 500 characters
        chunk_size = 500
        chunks = [line[i:i + chunk_size] for i in range(0, len(line), chunk_size)]

        translated_chunks = []
        for chunk in chunks:
            translated_chunks.append(translator.translate(chunk))

        # Join the translated chunks
        translated_line = ''.join(translated_chunks)
        translated_lines.append(translated_line)

    return '\n'.join(translated_lines)


def main(image_path, target_lang='en'):
    # Detect text from image
    text = detect_text(image_path)
    print(f"Detected Text: {text}")

    # Preprocess text to handle hyphenated words
    preprocessed_text = preprocess_text(text)
    print(f"Preprocessed Text: {preprocessed_text}")

    # Translate text
    translated_text = translate_text(preprocessed_text, target_lang)
    print(f"Translated Text: {translated_text}")


if __name__ == "__main__":
    # Example usage:
    image_path = r"D:\Computer Vision\OCR_Images\image.jpg"
    target_lang = 'pt-br'  # Change to any language code you want to translate to
    main(image_path, target_lang)
