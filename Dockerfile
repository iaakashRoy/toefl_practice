# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World
ENV GROQ_API_KEY="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"

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]