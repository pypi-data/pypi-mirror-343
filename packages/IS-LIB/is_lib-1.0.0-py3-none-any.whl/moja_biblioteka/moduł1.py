from flask import session


def login_req(func):
    def wrapper(*args, **kwargs):
        if session.get('username'):
            result = func(*args, **kwargs)
            return result
        else:
            return("NIE MA KURWA    ")
    wrapper.__name__ = func.__name__

    return wrapper
