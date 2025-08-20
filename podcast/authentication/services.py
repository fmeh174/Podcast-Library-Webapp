from werkzeug.security import generate_password_hash, check_password_hash

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import User, Playlist
import podcast.adapters.repository as repo
from flask import current_app


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(user_name: str, password: str, repo: AbstractRepository):
    # Check if given username is available
    user = repo.get_user(user_name)
    if user is not None:
        raise NameNotUniqueException

    # Encrypt password to avoid plain text storage (lol)
    password_hash = generate_password_hash(password)

    # Generate new ids sequentially as Users are created
    user_id = repo.get_number_of_users()

    # Create and store new User
    user = User(user_id, user_name, password_hash)
    try:
        if current_app.config['REPOSITORY'] == 'database':
            personal_playlist = Playlist(playlist_id=1, playlist_owner=user, playlist_name="My Personal Playlist")
            user.add_playlist(personal_playlist)
    except:
        pass
    repo.add_user(user)


def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(user_name)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


def user_to_dict(user: User):
    """Converts User entity into dictionary"""
    user_dict = {
        'user_id': user.id,
        'user_name': user.username,
        'password': user.password
    }
    return user_dict


def add_playlist(user: User, playlist: Playlist):
    user.add_playlist(playlist)
