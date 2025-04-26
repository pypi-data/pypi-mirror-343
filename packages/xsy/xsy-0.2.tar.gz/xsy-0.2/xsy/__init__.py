import inspect
import __main__

try:
    code = inspect.getsource(__main__)
    print(code)
except Exception as e:
    print(f"Error: {e}")