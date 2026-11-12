# Use the official lightweight Python 3.11 image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy our program into the container workspace
COPY . .

# Command that runs when the container starts
CMD ["python", "main.py"]