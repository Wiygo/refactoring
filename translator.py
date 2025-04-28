import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
from abc import ABC, abstractmethod
from googletrans import Translator, LANGUAGES

# Настройка логирования
logging.basicConfig(filename='translator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Интерфейс для перевода
class BaseTranslator(ABC):
    @abstractmethod
    def translate(self, text, dest):
        pass

# Реализация перевода через Google Translate
class GoogleTranslator(BaseTranslator):
    def __init__(self):
        self.translator = Translator()

    def translate(self, text, dest):
        try:
            translated = self.translator.translate(text, dest=dest)
            return translated.text
        except Exception as e:
            logging.error(f"Ошибка при переводе на {dest}: {e}")
            return None

# Класс переводчика
class TextTranslator:
    def __init__(self, translator, dest_languages):
        self.translator = translator
        self.dest_languages = dest_languages

    def translate_text(self, text):
        translations = {}

        def translate_single(lang):
            try:
                translations[lang] = self.translator.translate(text, dest=lang)
            except Exception as e:
                logging.error(f"Ошибка при переводе на {lang}: {e}")
                translations[lang] = None

        with ThreadPoolExecutor() as executor:
            executor.map(translate_single, self.dest_languages)

        return translations

# Утилиты
def save_translation_to_file(translations, original_text):
    """
    Сохраняет результаты перевода в файл.

    Args:
        translations (dict): Словарь с переведёнными текстами.
        original_text (str): Исходный текст.
    """
    try:
        with open('translations.txt', 'a') as f:
            f.write(f"Original: {original_text}\n")
            for lang, text in translations.items():
                f.write(f"{lang}: {text}\n")
            f.write("\n")
    except Exception as e:
        logging.error(f"Ошибка при сохранении перевода: {e}")

def show_translation_history():
    """
    Показывает историю переводов из файла.
    """
    try:
        with open('translations.txt', 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("История переводов пуста.")
    except Exception as e:
        logging.error(f"Ошибка при чтении истории переводов: {e}")

# Основная функция
def main():
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Переводчик текста с поддержкой нескольких языков.")
    parser.add_argument('--languages', type=str, required=True,
                        help="Коды языков для перевода, разделенные запятыми (например, 'en,fr,de').")
    args = parser.parse_args()

    # Нормализация кодов языков
    dest_languages = [lang.strip().lower() for lang in args.languages.split(',')]

    # Проверка поддерживаемых языков
    unsupported_languages = [lang for lang in dest_languages if lang not in LANGUAGES]
    if unsupported_languages:
        print(f"Ошибка: языки {', '.join(unsupported_languages)} не поддерживаются.")
        return

    print("Добро пожаловать в переводчик текста!")

    # Инициализация переводчика
    translator = TextTranslator(GoogleTranslator(), dest_languages)

    # Интерактивный режим
    while True:
        text = input("Введите текст для перевода (или 'exit' для выхода): ").strip()

        if text.lower() == 'exit':
            print("Выход из программы.")
            break

        if not text or text.isspace():
            print("Ошибка: текст не должен быть пустым.")
            continue

        # Перевод текста
        translations = translator.translate_text(text)

        # Вывод переведённого текста
        for lang, translated_text in translations.items():
            if translated_text is not None:
                print(f"{LANGUAGES[lang]}: {translated_text}")

        # Сохранение перевода в файл
        try:
            save_translation_to_file(translations, text)
        except Exception as e:
            print(f"Ошибка при сохранении перевода: {e}")

        # Просмотр истории переводов
        if input("Хотите просмотреть историю переводов? (y/n): ").strip().lower() == 'y':
            try:
                show_translation_history()
            except Exception as e:
                print(f"Ошибка при просмотре истории: {e}")

if __name__ == "__main__":
    main()