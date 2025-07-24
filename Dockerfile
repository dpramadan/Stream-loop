FROM python:3.10-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Set workdir
WORKDIR /app

# Copy semua file
COPY . .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan Flask
CMD ["python", "app.py"]

