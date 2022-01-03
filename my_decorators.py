from datetime import datetime as dt
import functools


def improve_decor(path: str):
    def logger(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timing = dt.now().strftime('%Y-%M-%d %H:%M:%S')
            result = func(*args, **kwargs)
            func_name = func.__name__
            log_string = f'call time: <{timing}>; function name: <{func_name}>; args: <{args}, {kwargs}>; return: <{result}>\n'
            with open(path, mode='a') as f:
                f.writelines(log_string)
            return result
        return wrapper
    return logger


decor = improve_decor('new.txt')


@decor
def multiply(a, b):
    return a**b


print(multiply(2, 5))



