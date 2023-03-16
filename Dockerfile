# Use the slim version of Python 3.10 to reduce the image size
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set the application home directory
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copy only the requirements.txt file first, to leverage Docker's layer caching
# This way, the dependencies installation will only happen if there's a change in the requirements.txt file
COPY requirements.txt ./

# Install the required packages and clean up the apt cache to reduce the image size
# Removed python3-pip from the apt-get install command since it's already included in the python:3.10-slim base image
# Added --no-install-recommends to the apt-get install command to minimize the number of additional packages installed
# Added --no-cache-dir to the pip3 install command to prevent caching the pip packages, reducing the image size
# Cleaned up the apt cache using apt-get clean and removed the apt lists with rm -rf /var/lib/apt/lists/* to further reduce the image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg libavcodec-extra && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . ./

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind '0.0.0:8080' --workers 1 --threads 8 --timeout 0 main:app
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
