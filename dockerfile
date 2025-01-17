# Start with a Python base image
FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your entire project
COPY . /app
WORKDIR /app

# Set the command to start your bot
CMD ["python", "bot.py"]
