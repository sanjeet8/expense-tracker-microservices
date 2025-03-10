# Use Python 3.12 as base image
FROM python:3.12

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install dependencies inside virtual environment
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port for Django service
EXPOSE 8004

# Command to start Django application
CMD ["/bin/bash", "-c", ". venv/bin/activate && python manage.py migrate && python manage.py runserver 0.0.0.0:8004"]
