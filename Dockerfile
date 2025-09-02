FROM python:3.11.4-slim

# Set working directory
WORKDIR /app

# Install system dependencies (Postgres, Pillow, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt .

# Install Python deps
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8080

# Start Django app with Gunicorn
CMD gunicorn jobMonitoringApp.wsgi:application --bind 0.0.0.0:8080
