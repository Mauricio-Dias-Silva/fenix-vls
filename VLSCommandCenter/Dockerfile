# Fenix VLS - Dockerfile for Cloud Run Deployment
# Multi-stage build for a lean production image

FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Copy the parent core/ folder which has quantum_drive.py and airframe.py
# Cloud Run sees /app as the root, so we need to add it to PYTHONPATH
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Collect static files for production (whitenoise serves them)
RUN python manage.py collectstatic --noinput

# Cloud Run uses PORT env variable. Gunicorn binds to it.
ENV PORT=8080

# Run the application with Gunicorn (production WSGI server)
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 VLSCommandCenter.wsgi:application
