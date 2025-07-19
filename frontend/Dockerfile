# Use an official lightweight Python image
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port Gunicorn will run on
EXPOSE 5001

# Use Gunicorn to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "main:app"] 