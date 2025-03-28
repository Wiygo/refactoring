import sys
import json
from googletrans import Translator, LANGUAGES
import argparse
import os

history = []

def print_supported_languages():
    """Выводит поддерживаемые языки."""
    print("Поддерживаемые языки:")
    for lang_code, lang_name in LANGUAGES.items():
        print(f"{lang_code}: {lang_name}")

def translate_text(text, dest_languages):
    """Переводит текст на указанные языки.

    Args:
        text (str): Текст для перевода.
        dest_languages (list): Список кодов языков для перевода.

    Returns:
        dict: Словарь с переведёнными текстами.
    """
    translator = Translator()
    translations = {}
    
    for lang in dest_languages:
        try:
            translated = translator.translate(text, dest=lang)
            translations[lang] = translated.text
        except Exception as e:
            print(f"Ошибка при переводе на {lang}: {e}")
            translations[lang] = None
            
    return translations

def save_translation_to_file(translations, original_text):
    """Сохраняет переведённый текст в файл.

    Args:
        translations (dict): Словарь с переведёнными текстами.
        original_text (str): Исходный текст.
    """
    filename = "translations.json"
    
    # Проверка существования файла и загрузка истории
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            history_data = json.load(f)
    else:
        history_data = []
    
    # Добавление нового перевода в историю
    history_entry = {
        "original": original_text,
        "translations": translations
    }
    
    history_data.append(history_entry)
    
    with open(filename, 'w') as f:
        json.dump(history_data, f, ensure_ascii=False, indent=4)

def show_translation_history():
    """Показывает историю переводов из файла."""
    filename = "translations.json"
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            history_data = json.load(f)
            for entry in history_data:
                print(f"Исходный текст: {entry['original']}")
                for lang, translation in entry['translations'].items():
                    print(f"{LANGUAGES[lang]}: {translation}")
                print("-" * 40)
    else:
        print("История переводов пуста.")

def main():
    parser = argparse.ArgumentParser(description="Переводчик текста с поддержкой нескольких языков.")
    
    parser.add_argument('--languages', type=str, required=True,
                        help="Коды языков для перевода, разделенные запятыми (например, 'en,fr,de').")
    
    args = parser.parse_args()
    
    dest_languages = args.languages.split(',')
    
    for lang in dest_languages:
        if lang not in LANGUAGES:
            print(f"Ошибка: язык '{lang}' не поддерживается.")
            return
    
    print("Добро пожаловать в переводчик текста!")
    
    while True:
        text = input("Введите текст для перевода (или 'exit' для выхода): ").strip()
        
        if text.lower() == 'exit':
            print("Выход из программы.")
            break
        
        if not text:
            print("Ошибка: текст не должен быть пустым.")
            continue

        translations = translate_text(text, dest_languages)
        
        for lang, translated_text in translations.items():
            if translated_text is not None:
                print(f"{LANGUAGES[lang]}: {translated_text}")
        
        save_translation_to_file(translations, text)
        if input("Хотите просмотреть историю переводов? (y/n): ").strip().lower() == 'y':
            show_translation_history()

if __name__ == "__main__":
    main()

