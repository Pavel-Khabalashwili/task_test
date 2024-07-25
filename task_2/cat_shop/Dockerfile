# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . .

# Указываем команду запуска
CMD ["sh", "-c", "sleep 15 && python app.py"]
