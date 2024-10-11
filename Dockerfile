# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Install Allure for report generation and other dependencies
RUN apt-get update && \
    apt-get install -y openjdk-11-jre && \
    pip install allure-pytest && \
    apt-get clean

# Set environment variables if needed
ENV PYTHONPATH=/app

# Run pytest and generate Allure results
CMD ["pytest", "--alluredir=allure-results"]
