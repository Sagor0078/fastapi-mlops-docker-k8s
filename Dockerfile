# Base image
FROM python:3.7

# Set working directory
WORKDIR /app

# Copy files
COPY main.py /app
COPY requirements.txt /app
COPY model /app/model
COPY utils /app/utils

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
