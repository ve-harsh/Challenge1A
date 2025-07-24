# Use official Python image (must match AMD64 requirement)
FROM python:3.10-slim

WORKDIR /app

# Set working directory
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy English model
RUN python -m spacy download en_core_web_sm

# Copy all project files
COPY . .

# Create I/O folders (safe fallback)
RUN mkdir -p input output

# Run main script
CMD ["python", "main.py"]
