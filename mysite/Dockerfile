# Используйте официальный образ Python как базовый
FROM python:3.11

# Установите рабочую директорию в контейнере
WORKDIR /app

# Установите зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Установите netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd

# Копируйте исходный код проекта в контейнер
COPY . .

# Копируйте скрипт ожидания в контейнер
COPY wait-for-it.sh ./
RUN chmod +x wait-for-it.sh

# Откройте порт 8000 для внешнего мира
EXPOSE 8000

# Запустите сервер разработки Django с ожиданием
CMD ["./wait-for-it.sh", "db:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]