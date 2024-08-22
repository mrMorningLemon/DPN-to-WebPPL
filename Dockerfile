# Use the official Python slim image
FROM python:3-slim

# Update package lists (optional, may not be necessary with newer versions)
RUN apt-get update

# Install nodejs and npm (if needed)
RUN apt-get install -y nodejs npm

# Copy your application files
COPY examples /examples
COPY pnml_to_webppl /pnml_to_webppl
COPY requirements.txt /requirements.txt

# Install webppl globally
RUN npm install -g webppl

# Upgrade pip and install requirements from requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --upgrade -r requirements.txt

# Set environment variable (if necessary)
ENV PYTHONPATH="${PYTHONPATH}:/pnml_to_webppl"
