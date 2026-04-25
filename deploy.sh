#!/bin/bash

PROJECT_DIR="/var/www/vkr-golodyaev"

cd $PROJECT_DIR || { echo "Ошибка: Директория не найдена"; exit 1; }

echo "--- Загружаем обновления из Git ---"
git reset --hard HEAD
git pull origin main

echo "--- Установка прав доступа ---"
PROJECT_DIR="/var/www/vkr-golodyaev/tests/web"
sudo chmod -R 755 $PROJECT_DIR
sudo chown www-data:www-data "$PROJECT_DIR/flask_session/"
cd "$PROJECT_DIR/instance/" || { echo "Ошибка: Папка instance не найдена"; exit 1; }
sudo chown golodyaev:www-data check.db .
sudo chmod 664 check.db
sudo chmod 775 .

echo "--- Перезапуск Apache ---"
sudo systemctl restart apache2

cd /var/www/vkr-golodyaev
sudo chmod 775 deploy.sh
echo "--- Готово! ---"