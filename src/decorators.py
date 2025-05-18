import functools
from datetime import datetime


def log(filename=None):
    """
    Декоратор для логирования выполнения функций.

    Args:
        filename: Опциональное имя файла для записи логов (str или None)
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"{timestamp} - {func_name}"

            try:
                result = func(*args, **kwargs)
                success_message = f"{log_message} ok. Result: {result}\n"

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(success_message)
                else:
                    print(success_message, end='')

                return result

            except Exception as e:
                error_message = (
                    f"{log_message} error: {type(e).__name__}: {str(e)}. "
                    f"Inputs: {args}, {kwargs}\n"
                )

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(error_message)
                else:
                    print(error_message, end='')

                raise

        return wrapper

    return decorator

@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)