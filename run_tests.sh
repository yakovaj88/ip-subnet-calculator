#!/bin/bash

set -e

echo "Сборка Docker-образа для тестирования..."

docker build -t test-image -f Dockerfile.test .

echo "Запуск тестов внутри Docker-контейнера..."

docker run --rm test-image
