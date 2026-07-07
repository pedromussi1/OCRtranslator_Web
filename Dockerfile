# Use the official Python image (3.11 to match the pinned dependencies)
FROM python:3.11-slim

# Install Tesseract, OpenCV dependencies, and other necessary libraries
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Writable dirs for runtime uploads and Argos model downloads (works whether the host
# runs the container as root or a non-root user).
ENV ARGOS_PACKAGES_DIR=/tmp/argos
RUN mkdir -p static/uploads /tmp/argos && chmod -R 777 static/uploads /tmp/argos

EXPOSE 5000

# Serve with gunicorn. Generous timeout: the first translation to a new language downloads
# its model (~100-200 MB) before responding.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "300", "app:app"]
