# Use a specific version for the base image
FROM python:3.12.2-slim AS build-env

# Set working directory
WORKDIR /api

# Install build utilities and pip dependencies
RUN apt-get update -y && \
    apt-get install -y build-essential && \
    pip install --upgrade pip

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary code files and resources
COPY api/ ./api/

# Actual runtime image
FROM python:3.12.2-slim

# Set working directory
WORKDIR /api

# Copy from build environment
COPY --from=build-env /api /api

# Command to run the application
CMD ["unicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]