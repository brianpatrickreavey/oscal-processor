#!/bin/bash
# Stop and remove the running OSCAL Processor container

container_id=$(docker ps -q --filter ancestor=oscal-processor)

if [ -z "$container_id" ]; then
  echo "No running OSCAL Processor container found."
else
  docker stop $container_id
  docker rm $container_id
  echo "OSCAL Processor container stopped and removed."
fi
