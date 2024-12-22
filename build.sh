#!/bin/bash

echo "Building and starting the service..."

# Останавливаем все запущенные контейнеры
docker-compose down

# Собираем образы и запускаем сервисы
docker-compose up --build

# Проверяем, запущен ли сервис
docker-compose ps

echo "Service is running at http://localhost:5000"
