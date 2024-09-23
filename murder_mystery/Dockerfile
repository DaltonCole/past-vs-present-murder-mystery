# Use an official Python runtime as a parent image
FROM python:3.12
#FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir

# Copy the project code into the container
COPY . /app/
