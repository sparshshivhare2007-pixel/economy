FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ffmpeg \
    build-essential \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Copy all repo files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run bot
CMD bash start
