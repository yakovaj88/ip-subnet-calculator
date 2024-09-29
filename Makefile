# Makefile

# Цель для сборки тестового Docker-образа
build-test-image:
	docker build -t test-image -f Dockerfile.test .

# Цель для запуска тестов в Docker-контейнере
test: build-test-image
	docker run --rm test-image

# Цель для сборки основного Docker-образа
build:
	docker build -t your-image-name .

# Цель для запуска приложения в Docker-контейнере
run:
	docker run --rm your-image-name
