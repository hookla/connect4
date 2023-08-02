import time

def time_it(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        print(f"{function.__name__} ran in: {end_time - start_time} secs")
        return result
    return wrapper
