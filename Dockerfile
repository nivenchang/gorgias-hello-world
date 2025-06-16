# Dockerfile
# Instructions to build the Python environment for your backend app.

# Use an official lightweight Python image.
FROM python:3.9-slim

# Set the working directory inside the container.
WORKDIR /app

# Copy the file that lists the Python dependencies.
COPY requirements.txt .

# Install the dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container.
COPY . .

# Command to run the application using Gunicorn, a production-ready web server.
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]