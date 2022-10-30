import time
 
def calculate_time(func):
    '''
    Decorator for time calculate
    '''
     
    def wrapper(*args, **kwargs):
 
        begin = time.time()
        func(*args, **kwargs)
        end = time.time()
        duration = end - begin

        return duration

    return wrapper
 