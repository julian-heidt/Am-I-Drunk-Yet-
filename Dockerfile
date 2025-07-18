# ---- Base Stage ----
# Use an official lightweight Python image. This ensures we have the correct Python version.
FROM python:3.9-slim as base

# Set environment variables for a clean, non-interactive build
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Set the working directory
WORKDIR /app

# ---- Builder Stage ----
# This stage creates the virtual environment and installs dependencies into it.
FROM base as builder

# Create a virtual environment in /opt/venv
RUN python -m venv /opt/venv

# Copy and install dependencies into the venv
COPY requirements.txt .
RUN /opt/venv/bin/pip install -r requirements.txt

# ---- Production Stage ----
# This is the final, clean image for production.
FROM base as production

# Create a non-root user to run the application for better security
RUN addgroup --system app && adduser --system --group app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code into the container
COPY . .

# Change ownership of the app directory to the new user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Add the venv to the PATH, so commands run from the venv by default
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port the app runs on
EXPOSE 8000

# Run the application using Gunicorn from the virtual environment
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:8000"] 