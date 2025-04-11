import unittest
from unittest.mock import patch, MagicMock
from translator import TextTranslator

class TestTextTranslator(unittest.TestCase):

    def setUp(self):
        self.languages = ['en', 'fr', 'de']
        self.translator = TextTranslator(self.languages)

    def mock_translate_side_effect(self, translations):
        """
        Helper method to create a side effect for mocking translate calls.
        :param translations: List of translated texts corresponding to the languages.
        :return: A list of MagicMock objects with 'text' attributes set to translations.
        """
        return [MagicMock(text=text) for text in translations]

    @patch('googletrans.Translator.translate')
    def test_translate_text_success(self, mock_translate):
        mock_translate.side_effect = self.mock_translate_side_effect(['Hello', 'Bonjour', 'Hallo'])
        
        result = self.translator.translate_text("Hello")
        
        expected_result = {lang: text for lang, text in zip(self.languages, ['Hello', 'Bonjour', 'Hallo'])}
        
        self.assertEqual(result, expected_result)

    @patch('googletrans.Translator.translate')
    def test_translate_text_failure(self, mock_translate):
        mock_translate.side_effect = Exception("Translation Error")
        
        result = self.translator.translate_text("Hello")
        
        expected_result = {lang: None for lang in self.languages}
        
        self.assertEqual(result, expected_result)

    @patch('googletrans.Translator.translate')
    def test_translate_empty_text(self, mock_translate):
        mock_translate.side_effect = self.mock_translate_side_effect(['', '', ''])
        
        result = self.translator.translate_text("")
        
        expected_result = {lang: '' for lang in self.languages}
        
        self.assertEqual(result, expected_result)

    @patch('googletrans.Translator.translate')
    def test_partial_translation_failure(self, mock_translate):
        mock_translate.side_effect = [
            MagicMock(text='Hello'),
            Exception("Translation Error"),
            Exception("Translation Error")
        ]
        
        result = self.translator.translate_text("Hello")
        
        expected_result = {
            'en': 'Hello',
            'fr': None,
            'de': None
        }
        
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()