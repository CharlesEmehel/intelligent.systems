# Use the official Python image as base
# FROM python:3.9-slim

# Runtime Parent Image
FROM python:3.10.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set or Create the  Working Directory in the Container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Copy current Directory contents into container working directory:/app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port to the outside world
EXPOSE 5001

# Define environment variable
ENV FLASK_APP run.py

#Run app.py when the container runs
CMD ["python3", "run.py"]
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]