# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy source code
COPY src/webserver/ /app/webserver/
COPY src/output/ /app/output/
COPY temp/ /app/temp/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port (default for http.server is 8000)
EXPOSE 8000

# Set default log path
ENV LOG_PATH=/app/temp/webserver.log

# Start the webserver, redirecting logs to LOG_PATH
CMD python -m http.server 8000 --directory /app/webserver > "$LOG_PATH" 2>&1
