# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary system dependencies, including PortAudio
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    portaudio19-dev

# Install pip, upgrade to the latest version
RUN pip install --upgrade pip

# Install Python dependencies from requirements.txt and sounddevice
RUN pip install -r requirements.txt
RUN pip install sounddevice

# Expose port 8501 for Streamlit (default port)
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]