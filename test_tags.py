from ts_tokenizer.token_handler import TokenPreProcess, TokenProcessor
from ts_tokenizer.char_fix import CharFix

import re

pattern = r"^([\(]+)([^\)]+)([\)]+)(.*)$"

word = "(ve)yeni"

def is_initial_parenthesis(word: str):
    result = re.match(pattern, word)

    if result:
        parenthesis_content = str(result.group(1) + result.group(2) + result.group(3))
        processed_parenthesis = TokenPreProcess.is_in_parenthesis(parenthesis_content)
        remaining_part = result.group(4).strip()
        return processed_parenthesis, TokenProcessor.process_token(remaining_part)

#print(is_initial_parenthesis(word))

print(word.split(")"))