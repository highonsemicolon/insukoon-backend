FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nginx \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files to the container
COPY . /app/

# Expose ports
EXPOSE 8000

# Run Django migrations and start the server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py populate_prices && python manage.py runserver 0.0.0.0:8000"]
