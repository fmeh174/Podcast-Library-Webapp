from datetime import datetime

import pytest

from podcast.authentication.services import AuthenticationException
from podcast.authentication import services as auth_services


def test_can_add_user(in_memory_repo):
    new_user_name = "Mario"
    new_password = "MushroomKingdom123"

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name.lower()

    # Check that password has been encrypted
    assert user_as_dict['password'].startswith('scrypt:32768')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = "Luigi"
    password = "PolterGust5000"

    auth_services.add_user(user_name, password, in_memory_repo)

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'Wario'
    new_password = "IHateMario123"

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = "Waluigi"
    invalid_password = "IHaveNoNumbers!"

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, invalid_password, in_memory_repo)
