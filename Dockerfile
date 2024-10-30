# Use the official Python image as a base
FROM python:3.9-slim

# Install required system packages
RUN apt-get update && \
    apt-get install -y stress-ng iperf3 sysbench && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the local Python script to the container
COPY stress_test.py /app/stress_test.py

# Run the Python script when the container starts
CMD ["python", "stress_test.py"]