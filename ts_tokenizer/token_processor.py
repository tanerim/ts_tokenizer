import inspect
from .token_preprocess import TokenPreProcess
class TokenProcessor:

    def __init__(self):
        pass

    @staticmethod
    def run_all(word):
        results = {}
        for method_name in dir(TokenPreProcess):
            method = getattr(TokenPreProcess, method_name)
            # Skip special methods and built-in types
            if callable(method) and not method_name.startswith('__'):
                try:
                    # Check if the method requires one argument
                    if len(inspect.signature(method).parameters) == 1:
                        result = method(word)
                        if result:
                            results[method_name] = result
                except ValueError:
                    # Skip methods that don't have signatures (like built-ins)
                    continue
        return results if results else None