#!/usr/bin/env python3
"""Генерация изображений через Gemini API (модель gemini-2.5-flash-image).

Использование:
    GEMINI_API_KEY=... python3 gemini_image.py "описание картинки" output.png

Ключ берётся из переменной окружения GEMINI_API_KEY.
Зависимостей нет — только стандартная библиотека Python.
"""

import base64
import json
import os
import sys
import urllib.error
import urllib.request

MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent"
)


def generate_image(prompt: str, out_path: str, api_key: str) -> None:
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = json.load(response)
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", errors="replace")
        sys.exit(f"Ошибка API ({err.code}): {detail}")

    for candidate in body.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            inline = part.get("inlineData")
            if inline and inline.get("data"):
                with open(out_path, "wb") as fh:
                    fh.write(base64.b64decode(inline["data"]))
                print(f"Изображение сохранено: {out_path}")
                return
            if part.get("text"):
                print(part["text"])

    sys.exit("В ответе не оказалось изображения — попробуйте другой запрос.")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('Использование: python3 gemini_image.py "описание" [файл.png]')
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit("Не задана переменная окружения GEMINI_API_KEY.")
    prompt = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "image.png"
    generate_image(prompt, out_path, api_key)


if __name__ == "__main__":
    main()
