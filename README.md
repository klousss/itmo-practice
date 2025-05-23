# Multilanguage OCR Service

Контейнеризированный OCR-сервис на базе модели Surya (90+ языков), упакованный в Docker.

## Обзор

- **Backend**: FastAPI, обрабатывает POST `/ocr` и возвращает распознанный текст.
- **Frontend**: простая HTML/JS-страница, встроенная в FastAPI (`GET /`).
- **OCR-модель**: Surya (detector + recognizer) из Hugging Face.
- **Контейнеризация**: Docker + docker-compose.

## Быстрый старт

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/klousss/itmo-practice.git
   cd itmo-practice

2. Соберите и запустите контейнер:
    docker compose up --build

3. Откройте в браузере
    http://localhost:8000/

4. Выберите изображение и нажмите «Распознать» — получите JSON-ответ с полем text.
    