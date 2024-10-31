import unittest
from ts_tokenizer.token_handler import TokenPreProcess


class TestTokenPreProcess(unittest.TestCase):

    def test_is_mention(self):
        words = ['@tanerim', 'user', '@tscorpus', 'invalid']
        expected_results = [('@tanerim', 'Mention'), None, ('@tscorpus', 'Mention'), None]

        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_mention(word), expected)

    def test_is_hashtag(self):
        words = ['#hashtag', 'nohashtag', '#12345', '#invalid!']
        expected_results = [('#hashtag', 'Hashtag'), None, ('#12345', 'Hashtag'), None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_hashtag(word), expected)

    def test_is_in_quotes(self):
        words = ['"araba"', "'araba'", 'Araba']
        expected_results = [[('"', 'Punc'), ('araba', 'Valid_Word'), ('"', 'Punc')],
                            [("'", 'Punc'), ('araba', 'Valid_Word'), ("'", 'Punc')],
                            None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_in_quotes(word), expected)

    def test_is_in_parenthesis(self):
        words = ['(parantez)', '(parantez', 'no)']
        expected_results = [[('(', 'Punc'), ('parantez', 'Valid_Word'), (')', 'Punc')], None, None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_in_parenthesis(word), expected)

    def test_is_hour(self):
        words = ['12:30', '25:00', '5:99']
        expected_results = [('12:30', 'Hour'), None, None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_hour(word), expected)

    def test_is_date(self):
        words = ['12/05/2023', '31.02.2020', '32.14.2024']
        expected_results = [('12/05/2023', 'Date'), None, None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_date(word), expected)

    def test_is_percentage_numbers(self):
        words = ['%50', '50%', '%abc']
        expected_results = [('%50', 'Percentage_Numbers'), ('50%', 'Percentage_Numbers'), None]
        for word, expected in zip(words, expected_results):
            if isinstance(expected, list):  # For cases where multiple tokens are returned
                self.assertEqual(TokenPreProcess.is_percentage_numbers_chars(word), expected)
            else:  # For single token results
                self.assertEqual(TokenPreProcess.is_percentage_numbers(word), expected)

    def test_is_percentage_numbers_chars(self):
        words = ['%50USD', 'USD%50',]
        expected_results = [[('%50', 'Percentage_Numbers'), ('USD', 'Abbr')], None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_percentage_numbers_chars(word), expected)

    def test_is_roman_number(self):
        words = ['X', 'V', '123', 'invalid']
        expected_results = [('X', 'Roman_Number'), ('V', 'Roman_Number'), None, None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_roman_number(word), expected)

    def test_is_email_punc(self):
        words = ['.test@example.com.', 'test@example.com.', 'invalid']
        expected_results = [
            [('.', 'Punc'), ('test@example.com', 'Email'), ('.', 'Punc')],
            [('test@example.com', 'Email'), ('.', 'Punc')],
            None
        ]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_email_punc(word), expected)

    def test_is_email(self):
        words = ['test@example.com', 'user@domain', 'invalid_email']
        expected_results = [('test@example.com', 'Email'), None, None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_email(word), expected)

    def test_is_url(self):
        words = ['http://example.com', 'www.test.com', 'not_a_url', 'https://example.com',]
        expected_results = [('http://example.com', 'URL'), ('www.test.com', 'URL'), None, ('https://example.com', 'URL')]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_url(word), expected)

    def test_is_copyright(self):
        words = ['©2023', '2023©', 'invalid']
        expected_results = [('©2023', 'Copyright'), ('2023©', 'Copyright'), None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_copyright(word), expected)

    def test_is_registered(self):
        words = ['®Ibanez', 'Fender®', 'invalid']
        expected_results = [('®Ibanez', 'Registered'), ('Fender®', 'Registered'), None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_registered(word), expected)

    def test_is_currency(self):
        words = ['$100', '100€', 'invalid']
        expected_results = [('$100', 'Currency'), ('100€', 'Currency'), None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_currency(word), expected)

    def test_is_abbr(self):
        words = ['vb', 'TBMM', 'invalid']
        expected_results = [('vb', 'Abbr'), ('TBMM', 'Abbr'), None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_abbr(word), expected)

    def test_is_in_lexicon(self):
        words = ['araba', 'ilamklamuli', 'arabalarındaki']
        expected_results = [('araba', 'Valid_Word'), None, ('arabalarındaki', 'Valid_Word')]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_in_lexicon(word), expected)

    def test_is_number(self):
        words = ['12345', 'invalid', '123.456', '123,456']
        expected_results = [('12345', 'Number'), None, None, None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_number(word), expected)

    def test_is_in_exceptions(self):
        words = ['dvd-rom', 'notexception', 'sosyo-demografik']
        expected_results = [('dvd-rom', 'Exception'), None, ('sosyo-demografik', 'Exception')]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_in_exceptions(word), expected)

    def test_is_in_eng_words(self):
        words = ['hello', 'notenglish', 'car']
        expected_results = [('hello', 'English_Word'), None, ('car', 'English_Word')]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_in_eng_words(word), expected)

    def test_is_smiley(self):
        words = [':)', ':D', 'invalid']
        expected_results = [(':)', 'Smiley'), (':D', 'Smiley'), None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_smiley(word), expected)

    def test_is_multiple_smiley(self):
        words = [':):)', ':-)', 'invalid']
        expected_results = [(':):)', 'Multiple_Smiley'), None, None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_multiple_smiley(word), expected)

    def test_is_multiple_smiley_in(self):
        words = ['Heyyo:-):-)', ':-)', 'invalid', 'yes:):)']
        expected_results = [('Heyyo:-):-)', 'Multiple_Smiley_In'), None, None, ('yes:):)', 'Multiple_Smiley_In')]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_multiple_smiley_in(word), expected)

    def test_is_emoticon(self):
        words = ['🖤', ':(', '🥰']
        expected_results = [('🖤', 'Emoticon'), None, ('🥰', 'Emoticon')]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_emoticon(word), expected)

    def test_is_multiple_emoticon(self):
        words = ['🥰🥰', '🥰', '🖤🥰']
        expected_results = [('🥰🥰', 'Multiple_Emoticon'),  None, ('🖤🥰', 'Multiple_Emoticon')]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_multiple_emoticon(word), expected)

    def test_is_fsp(self):
        words = ['araba.']
        expected_results = [[('araba', 'Valid_Word'), ('.', 'Punc')]]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_fsp(word), expected)

    def test_is_isp(self):
        words = ['.araba']
        expected_results = [[('.', 'Punc'), ('araba', 'Valid_Word')]]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_isp(word), expected)

    def test_is_mssp(self):
        words = ['.araba.', '..araba..', '.']
        expected_results = [[('.', 'Punc'), ('araba', 'Valid_Word'), ('.', 'Punc')], None, None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_mssp(word), expected)

    def test_is_msp(self):
        words = ['...araba...', 'araba']
        expected_results = [[('...', 'Punc'), ('araba', 'Valid_Word'), ('...', 'Punc')], None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_msp(word), expected)

    def test_is_imp(self):
        words = ['...araba', 'araba...']
        expected_results = [[('...', 'Punc'), ('araba', 'Valid_Word')], None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_imp(word), expected)

    def test_is_fmp(self):
        words = ['araba...', '...araba', 'Geldim(!)']
        expected_results = [[('araba', 'Valid_Word'), ('...', 'Punc')], None, [('Geldim', 'Valid_Word'), ('(!)', 'Punc')]]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_fmp(word), expected)

    def test_is_apostrophed(self):
        words = ["Defne'nin", "Bengü\"nün", "Türkiye ́de"]
        expected_results = [("Defne'nin", 'Apostrophed'), None, ("Türkiye'de", 'Apostrophed')]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_apostrophed(word), expected)

    def test_is_non_latin(self):
        words = ['你好', '𝐆eldim']
        expected_results = [('你好', 'Non_Latin'), ('𝐆eldim', 'Non_Latin')]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_non_latin(word), expected)

    def test_is_one_char_fixable(self):
        words = ['gelmek¬te', 'valid', 'bili-yorum']
        expected_results = [('gelmekte', 'One_Char_Fixed'), None, ('biliyorum', 'One_Char_Fixed')]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_one_char_fixable(word), expected)

    def test_is_punc(self):
        words = ['!!!', 'invalid!', '(!)', '---']
        expected_results = [('!!!', 'Punc'), None, ('(!)', 'Punc'), ('---', 'Punc')]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_punc(word), expected)

    def test_is_underscored(self):
        words = ['word_123', '_yeni_', 'geçersiz_', '_geçersiz']
        expected_results = [('word_123', 'Alphanumeric_Underscored'), None, None, None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_underscored(word), expected)

    def test_is_three_or_more(self):
        words = ['-----', '.....', '!!']
        expected_results = [('-----', 'Three_Or_More'), ('.....', 'Three_Or_More'), None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_three_or_more(word), expected)

    def test_is_date_range(self):
        words = ['1990-1995', '1995-2000', '(invalid-range)']
        expected_results = [('1990-1995', 'Date_Range'), ('1995-2000', 'Date_Range'), None]
        for word, expected in zip(words, expected_results):
            self.assertEqual(TokenPreProcess.is_date_range(word), expected)


if __name__ == '__main__':
    unittest.main()
