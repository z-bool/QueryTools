from functools import wraps
from typing import Callable, Dict, Any


class TryMe:

    def __init__(self):
        self.exception_: Dict[Any, Callable] = {}

    def try_(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler = None
                for c in self.exception_.keys():
                    if isinstance(e, c):
                        handler = c

                if handler is None:
                    raise e
                # 将异常发生的函数和异常对象传入异常处理函数
                return self.exception_[handler](func, e)

        return wrapper

    def except_(self, *exceptions):
        def decorator(f):
            for e in exceptions:
                self.exception_[e] = f
            return f

        return decorator


tryme = TryMe()


@tryme.except_(Exception)
def handle_zero_division_error(func, e):
    print("error: ", func.__name__, str(e))
