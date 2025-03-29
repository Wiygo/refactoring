import unittest
from unittest.mock import patch, MagicMock
from translator import TextTranslator

class TestTextTranslator(unittest.TestCase):

    def setUp(self):
        self.languages = ['en', 'fr', 'de']
        self.translator = TextTranslator(self.languages)

    @patch('googletrans.Translator.translate')
    def test_translate_text_success(self, mock_translate):
        mock_translate.side_effect = [
            MagicMock(text='Hello'), 
            MagicMock(text='Bonjour'), 
            MagicMock(text='Hallo')
        ]
        
        result = self.translator.translate_text("Hello")
        
        expected_result = {
            'en': 'Hello',
            'fr': 'Bonjour',
            'de': 'Hallo'
        }
        
        self.assertEqual(result, expected_result)

    @patch('googletrans.Translator.translate')
    def test_translate_text_failure(self, mock_translate):
        mock_translate.side_effect = Exception("Translation Error")
        
        result = self.translator.translate_text("Hello")
        
        expected_result = {
            'en': None,
            'fr': None,
            'de': None
        }
        
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()