# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for psycopg and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt-get/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt 
    
# Copy the entire project into the container
COPY . .

# Collect static files for WhiteNoise static file serving
RUN python manage.py collectstatic --noinput || true

# Expose the port Django runs on
EXPOSE 8000

# Command to run the application using Gunicorn production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecommerce_project.wsgi:application"]