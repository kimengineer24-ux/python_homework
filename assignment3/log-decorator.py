import logging

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))


# Task 1: Writing and Testing a Decorator
def logger_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        logger.log(logging.INFO, f"function: {func.__name__}")
        logger.log(logging.INFO, f"positional parameters: {args if args else 'none'}")
        logger.log(logging.INFO, f"keyword parameters: {kwargs if kwargs else 'none'}")
        logger.log(logging.INFO, f"return: {result}")

        return result

    return wrapper


@logger_decorator
def hello_world():
    print("Hello, World!")


@logger_decorator
def positional_function(*args):
    return True


@logger_decorator
def keyword_function(**kwargs):
    return logger_decorator


hello_world()
positional_function(1, 2, 3, "Kimmie")
keyword_function(name="Kimmie", lesson=3, status="moving fast")