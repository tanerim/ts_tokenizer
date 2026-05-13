import unittest
from ts_tokenizer.tokenizer import tokenize


class TestTSTokenizer(unittest.TestCase):

    def test_tokenize_simple(self):
        input_text = "Parça ve bütün ilişkisi."
        expected_output = "Parça\nve\nbütün\nilişkisi\n."
        result = tokenize(input_text, return_format="tokenized")

        # Debugging output
        print("Generated:", result)
        print("Expected:", expected_output)

        # Assert that result is not None and matches expected output
        self.assertIsNotNone(result, "The result should not be None")
        self.assertEqual(result, expected_output)



if __name__ == '__main__':
    unittest.main()