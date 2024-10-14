from ts_tokenizer.token_handler import TokenProcessor

class oov_parser:
    def __init__(self):
        pass

    @staticmethod
    def isp_parser(word: str) -> tuple:
        if word[0] == ",":
            return TokenProcessor.process_token(word[1:])


word = ",yeniden,eski"

print(oov_parser.isp_parser(word))