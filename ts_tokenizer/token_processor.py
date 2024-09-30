from ts_tokenizer.token_preprocess import TokenPreProcess


class TokenProcessor:

    def __init__(self):
        pass

    @staticmethod
    def run_all(word):
        results = {}
        methods = [method_name for method_name in dir(TokenPreProcess) if
                   callable(getattr(TokenPreProcess, method_name)) and not method_name.startswith("__")]

        for method_name in methods:
            method = getattr(TokenPreProcess, method_name)
            if callable(method):
                try:
                    result = method(word)
                    results[method_name] = result
                except Exception as e:
                    print(f"Error in method {method_name}: {e}")
                    continue

        return results if results else None
