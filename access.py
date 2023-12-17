from functools import wraps
from flask import session, request, current_app


def login_req(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" in session:
            return func(*args, **kwargs)
        return "А вы не авторизовались"
    return wrapper


def group_req(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" in session:
            user_group = session.get("user_group")
            if user_group:
                access = current_app.config["access_config"]
                user_target = request.blueprint
                print(user_target)
                if user_group in access and user_target in access[user_group]:
                    return func(*args, **kwargs)
                return "Доступа нет"
        return "Авторизации нет"
    return wrapper
