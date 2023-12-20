FROM python:3.8-slim

# Install Python dependencies
RUN pip install redis pika

# Copy the listener script into the container
COPY listener_service.py /listener_service.py

# Command to run the service
CMD ["python", "/listener_service.py"]
