# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install SWI-Prolog and system dependencies
RUN apt-get update && apt-get install -y \
    swi-prolog \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Run the app using Gunicorn (production-grade server)
CMD gunicorn --bind 0.0.0.0:$PORT app:app