FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY . /app

# Optional: upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Default command
CMD ["python", "app/main.py"]
