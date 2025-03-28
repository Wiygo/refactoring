# utils.py
import json
import os
from googletrans import LANGUAGES

def print_supported_languages():
    """Выводит поддерживаемые языки."""
    print("Поддерживаемые языки:")
    for lang_code, lang_name in LANGUAGES.items():
        print(f"{lang_code}: {lang_name}")

def save_translation_to_file(translations, original_text, filename="translations.json"):
    """Сохраняет переведённый текст в файл.

    Args:
        translations (dict): Словарь с переведёнными текстами.
        original_text (str): Исходный текст.
        filename (str): Имя файла для сохранения истории переводов.
    """
    history_data = load_translation_history(filename)
    
    # Добавление нового перевода в историю
    history_entry = {
        "original": original_text,
        "translations": translations
    }
    
    history_data.append(history_entry)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, ensure_ascii=False, indent=4)

def load_translation_history(filename):
    """Загружает историю переводов из файла.

    Args:
        filename (str): Имя файла для загрузки истории переводов.

    Returns:
        list: Список историй переводов.
    """
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def show_translation_history(filename="translations.json"):
    """Показывает историю переводов из файла."""
    history_data = load_translation_history(filename)
    
    if history_data:
        for entry in history_data:
            print(f"Исходный текст: {entry['original']}")
            for lang, translation in entry['translations'].items():
                print(f"{LANGUAGES[lang]}: {translation}")
            print("-" * 40)
    else:
        print("История переводов пуста.")
