# Use the official Python image
FROM python:3.10-slim

# Install Tesseract, OpenCV dependencies, and other necessary libraries
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000
EXPOSE 5000

# Argos Translate downloads language models to this dir on first use; mount a volume
# here to persist them across restarts (otherwise they re-download).
ENV ARGOS_PACKAGES_DIR=/app/.argos

# Serve with gunicorn (production WSGI server) instead of the Flask dev server.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]
