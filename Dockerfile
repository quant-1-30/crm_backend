# Use the official Python image as a base image
# FROM python:3.9-slim
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN pip install --no-cache-dir curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    # Add Poetry to PATH
    export PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy only the dependency files to leverage Docker cache
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN /root/.local/bin/poetry install --no-root --no-dev

# Copy the rest of the application code into the image
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["/root/.local/bin/poetry", "run", "python", "crm_backend/main.py"]
