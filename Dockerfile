FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create __init__.py files for packages (if they don't exist)
RUN touch agents/__init__.py core/__init__.py memory/__init__.py tools/__init__.py

# Expose port
EXPOSE 7860

# Set environment variables for Hugging Face
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860
ENV GRADIO_SHARE=false

# Run the application
CMD ["python", "app.py"]
