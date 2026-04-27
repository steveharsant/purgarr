#!/usr/bin/env bash

version=$(awk -F\" '/__version__/ {print $2}' ./src/main.py | head -n1)
base_tag='ghcr.io/steveharsant/purgarr'

echo "$GITHUB_TOKEN" | docker login ghcr.io -u steveharsant --password-stdin

# Ensure a buildx builder with multi-platform support is available
docker buildx create --name multiarch --driver docker-container --use 2>/dev/null || \
  docker buildx use multiarch

docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag "$base_tag:latest" \
  --tag "$base_tag:$version" \
  --push \
  .

docker buildx rm multiarch 2>/dev/null || true
docker logout
