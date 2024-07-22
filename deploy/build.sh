#!/bin/bash

read -p "Do you want to rebuild the Docker image from scratch? This will take longer than using cached layers. (y/N): " rebuild

if [[ $rebuild =~ ^[Yy]$ ]]; then
    echo "Rebuilding the Docker image from scratch..."
    podman build --no-cache -t ghcr.io/medusa-ml/translatetribune:latest -f deploy/Dockerfile .
else
    echo "Building the Docker image using cached layers (if available)..."
    podman build -t ghcr.io/medusa-ml/translatetribune:latest -f deploy/Dockerfile .
fi
