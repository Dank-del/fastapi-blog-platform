# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the project files to the container
COPY . .

# Expose the port that the FastAPI application will listen on
EXPOSE 8000

# Set the command to run the FastAPI application
CMD ["python3", "main.py"]