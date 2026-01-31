# Указываем базовый образ Python
FROM python:3.14-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы проекта
COPY . .

# Обновляем pip и ставим зависимости
RUN python -m pip install --upgrade pip
RUN python -m pip install fastapi uvicorn prometheus-client

# Указываем команду запуска контейнера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
