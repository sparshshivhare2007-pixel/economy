# Base image (Python 3.10)
FROM python:3.10-slim

# Work directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy all files
COPY . .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python3", "main.py"]
