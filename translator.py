import argparse
from googletrans import Translator, LANGUAGES
from utils import print_supported_languages, save_translation_to_file, show_translation_history

class TextTranslator:
    def __init__(self, dest_languages):
        self.translator = Translator()
        self.dest_languages = dest_languages

    def translate_text(self, text):
        """Переводит текст на указанные языки.

        Args:
            text (str): Текст для перевода.

        Returns:
            dict: Словарь с переведёнными текстами.
        """
        translations = {}
        
        for lang in self.dest_languages:
            try:
                translated = self.translator.translate(text, dest=lang)
                translations[lang] = translated.text
            except Exception as e:
                print(f"Ошибка при переводе на {lang}: {e}")
                translations[lang] = None
                
        return translations

def main():
    parser = argparse.ArgumentParser(description="Переводчик текста с поддержкой нескольких языков.")
    
    parser.add_argument('--languages', type=str, required=True,
                        help="Коды языков для перевода, разделенные запятыми (например, 'en,fr,de').")
    
    args = parser.parse_args()
    
    dest_languages = args.languages.split(',')
    
    # Проверка поддерживаемых языков
    unsupported_languages = [lang for lang in dest_languages if lang not in LANGUAGES]
    if unsupported_languages:
        print(f"Ошибка: языки {', '.join(unsupported_languages)} не поддерживаются.")
        return
    
    print("Добро пожаловать в переводчик текста!")
    
    translator = TextTranslator(dest_languages)
    
    while True:
        text = input("Введите текст для перевода (или 'exit' для выхода): ").strip()
        
        if text.lower() == 'exit':
            print("Выход из программы.")
            break
        
        if not text:
            print("Ошибка: текст не должен быть пустым.")
            continue

        translations = translator.translate_text(text)
        
        for lang, translated_text in translations.items():
            if translated_text is not None:
                print(f"{LANGUAGES[lang]}: {translated_text}")
        
        save_translation_to_file(translations, text)
        
        if input("Хотите просмотреть историю переводов? (y/n): ").strip().lower() == 'y':
            show_translation_history()

if __name__ == "__main__":
    main()
