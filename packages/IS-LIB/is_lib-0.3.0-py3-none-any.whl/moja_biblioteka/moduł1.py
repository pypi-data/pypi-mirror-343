from flask import session


def login_req(func):
    def wrapper(*args, **kwargs):
        if session['username']:
            result = func(*args, **kwargs)
            return result
        else:
            return "Non logged user in that session."

    return wrapper
