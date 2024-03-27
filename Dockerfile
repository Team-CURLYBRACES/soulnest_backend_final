# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY ./requirements.txt ./app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r ./app/requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Run Gunicorn
CMD gunicorn soulnest.wsgi:application --bind 0.0.0.0:8000
