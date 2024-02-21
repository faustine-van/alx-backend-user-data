#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """Register user.

    Args:
        email (str): Email of the user.
        password (str): Password of user
    """
    data = {'email': email, 'password': password}
    r = requests.post('http://0.0.0.0:5000/users', data=data)

    assert r.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Login with wrong password.

    Args:
        email (str): Email of the user.
        password (str): Password of user
    """
    data = {'email': email, 'password': password}
    r = requests.post('http://0.0.0.0:5000/sessions', data=data)

    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """Login with correct login info

    Args:
        email (str): Email of the user.
        password (str): Password of user
    """
    data = {'email': email, 'password': password}
    r = requests.post('http://0.0.0.0:5000/sessions', data=data)
    if r.status_code == 200:
        return r.cookies.get('session_id')


def profile_unlogged() -> None:
    """Profile unlogged login info

    Args:
        email (str): Email of the user.
        password (str): Password of user
    """
    pass


def profile_logged(session_id: str) -> None:
    """Login with correct login info

    Args:
        email (str): Email of the user.
        password (str): Password of user
    """
    cookies = {'session_id': session_id}
    r = requests.post('http://0.0.0.0:5000/profile', cookies=cookies)
    r.status_code == 200


def log_out(session_id: str) -> None:
    """Logout with correct login info

    Args:
        session_id (str): session_id of the user.
    """
    cookies = {'session_id': session_id}
    r = requests.post('http://0.0.0.0:5000//sessions', cookies=cookies)
    r.status_code == 200


def reset_password_token(email: str) -> str:
    """reset password
    Args:
        email (str): Email of the user
    """
    data = {'email': email}
    r = requests.post('http://0.0.0.0:5000/reset_password', data=data)
    if r.status_code == 200:
        return r.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update password
    Args:
        email (str): Email of the user
        reset_token (str): token of user
        new_password (str): new password
    """
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    r = requests.post('http://0.0.0.0:5000/reset_password', data=data)
    r.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)