# Dockerfile for Django / Gunicorn
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only requirements first (better caching)
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt

# Now copy the rest of your Django code
COPY . /app

# Expose port 8000 inside the container (for internal Docker networking)
EXPOSE 8000

# By default, run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "root.wsgi"]
