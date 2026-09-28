# Генерация изображений через Gemini

Скрипт `gemini_image.py` генерирует изображения через Google Gemini API
(модель `gemini-2.5-flash-image`, она же Nano Banana). Зависимостей нет —
достаточно Python 3.

## Настройка

1. Получите бесплатный API-ключ: https://aistudio.google.com/apikey
   (нужен только аккаунт Google; у API есть бесплатный лимит).
2. Добавьте ключ в переменную окружения `GEMINI_API_KEY`.
   В облачной среде Claude Code: меню окружения в заголовке сессии →
   Edit → API credentials / environment variables.

## Использование

```bash
python3 gemini_image.py "кот в космосе, акварель" cat.png
```

Второй аргумент (имя файла) необязателен — по умолчанию `image.png`.
Модель можно сменить через переменную `GEMINI_IMAGE_MODEL`.
