from token_handler import TokenProcessor


class oov_parser:
    def __init__(self):
        pass

    @staticmethod
    def tokenize_oov(candidate: tuple) ->tuple:
        if type(candidate) is tuple:
            if candidate[1] == "OOV":
                return TokenProcessor.process_token(candidate[0])


#print(oov_parser.tokenize_oov(("oldu-bitti", "OOV")))