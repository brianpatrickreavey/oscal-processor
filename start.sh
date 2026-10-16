#!/bin/bash
# Build the Docker image
docker build -t oscal-processor .


# Set log path (default: temp/webserver.log)
LOG_PATH=${LOG_PATH:-$(pwd)/temp/webserver.log}

# Ensure log directory exists
LOG_DIR=$(dirname "$LOG_PATH")
mkdir -p "$LOG_DIR"

# Ensure temp directory exists
mkdir -p $(pwd)/temp

# Run the container in detached mode, mounting output and temp directories, and setting LOG_PATH
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/src/output:/app/output \
  -v $(pwd)/temp:/app/temp \
  -e LOG_PATH="/app/temp/$(basename $LOG_PATH)" \
  oscal-processor

# Wait for the webserver to be available
echo -n "Waiting for OSCAL Processor to start on port 8000"
until nc -z localhost 8000; do
  echo -n "."
  sleep 1
done
echo ""
echo "OSCAL Processor is running. Access it at http://localhost:8000"