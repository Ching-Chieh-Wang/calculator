from functools import wraps

def convert_integers():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            num1 = kwargs.get('num1')
            num2 = kwargs.get('num2')
            if isinstance(num1, float) and num1.is_integer():
                kwargs['num1'] = int(num1)
            if isinstance(num2, float) and num2.is_integer():
                kwargs['num2'] = int(num2)
            return f(*args, **kwargs)
        return wrapper
    return decorator
