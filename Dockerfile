# Use the official Python image as base
# FROM python:3.10.12
# FROM python:3.10-slim
# FROM python:3.10-alpine
# FROM python:3.9
FROM python:3.9
# python:3.10-buster # Debian Buster. It includes all the packages and features of Debian 10,
# python:3.10-bullseye # Debian Bullseye. It includes all the packages and features of Debian 11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set or Create the Working Directory in the Container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cython3 \
    openssl \
    libyaml-dev \
    nano \
    && apt-get clean

# Upgrade pip, setuptools, wheel and flask_wtf
# RUN pip install --upgrade pip setuptools wheel && pip install --upgrade flask_wtf
RUN pip install --upgrade pip setuptools wheel flask_wtf

# Install PyYAML with no build isolation
RUN pip install --no-build-isolation PyYAML==5.4.1

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy current Directory contents into container working directory:/app
COPY . /app

# Generate SSL certificates
RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"

# Expose port to the outside world
EXPOSE 5001

# Define environment variable
ENV FLASK_APP run.py

# Run app.py when the container runs
CMD ["python3", "run.py"]
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
