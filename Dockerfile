# Use Python 3.12.10
FROM python:3.12.10-slim

# Set work directory
WORKDIR /app

# # Install system dependencies needed for pip packages
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     gcc \
#     g++ \
#     python3-dev \
#     libffi-dev \
#     libssl-dev \
#     && rm -rf /var/lib/apt/lists/*

# Copy only the lock file first (caching)
COPY req-lock.txt .

# Install all Python dependencies FROM req-lock.txt
RUN pip install --no-cache-dir -r req-lock.txt

# Copy full project
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
