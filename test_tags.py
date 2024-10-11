from ts_tokenizer.token_handler import TokenPreProcess, TokenProcessor
from ts_tokenizer.char_fix import CharFix

word = "(ve)yeni"


print(TokenProcessor.process_token(word))