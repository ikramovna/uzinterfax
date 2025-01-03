# Start from a lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (for better Docker caching)
COPY requirements.txt /app/

# Install system dependencies & Python deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the project
COPY . /app

# Expose the port Gunicorn will run on
EXPOSE 8000

# Default command: run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "root.wsgi"]
