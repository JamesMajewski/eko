#!/bin/bash

# Build Docker image
docker build -t my-flask-app .

# Run Docker container
docker run -p 5000:5000 my-flask-app
