# Use the official Python image as a base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the script and requirements to the container
COPY . .

# Install dependencies
RUN pip install facebook-business 
# google-api-python-client Flask praw

# Define the command to run the script
CMD ["python", "main.py"]
