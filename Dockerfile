# Use the official Python image as a base image
# FROM python:3.9-slim
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry
#RUN curl -sSL https://install.python-poetry.org | python3 - && \
#    # Add Poetry to PATH
#    export PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the rest of the application code into the image
COPY . /app/

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip3 install poetry-1.7.1-py3-none-any.whl

RUN poetry lock --no-update && poetry install 
#RUN poetry install 

# Expose the port the app runs on
#EXPOSE 8000

# Command to run the application
#CMD ["/root/.local/bin/poetry", "run", "python", "crm_backend/main.py"]
CMD ["bash", "init.sh"]
