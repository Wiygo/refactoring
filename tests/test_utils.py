import unittest
import json
import os
from utils import save_translation_to_file, load_translation_history, show_translation_history

class TestUtils(unittest.TestCase):
    
    def setUp(self):
        self.test_filename = "test_translations.json"
        self.original_text = "Hello"
        self.translations = {"en": "Hello", "fr": "Bonjour", "de": "Hallo"}

    def tearDown(self):
        """Удаляем файл после теста."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_save_translation_to_file(self):
        save_translation_to_file(self.translations, self.original_text, self.test_filename)
        
        with open(self.test_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["original"], self.original_text)
        self.assertEqual(data[0]["translations"], self.translations)

    def test_load_translation_history_empty(self):
        history = load_translation_history(self.test_filename)
        self.assertEqual(history, [])

    def test_show_translation_history(self):
        save_translation_to_file(self.translations, self.original_text, self.test_filename)
        from io import StringIO
        import sys
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        show_translation_history(self.test_filename)
        
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        
        self.assertIn(self.original_text, output)
        for lang in self.translations:
            self.assertIn(self.translations[lang], output)

if __name__ == "__main__":
    unittest.main()