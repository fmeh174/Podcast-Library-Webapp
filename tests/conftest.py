import pytest

from podcast import create_app
from podcast.adapters.memory_repository import MemoryRepository
from podcast.adapters.repo_populate import populate

from path_utils.utils import get_project_root


# Gets data from test data folder, not the main data folder in the podcast directory.
TEST_DATA_PATH = get_project_root() / "tests" / "data"
TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///podcast-test.db'

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False,
        'REPOSITORY': "memory"
    })
    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='Mario', password='ILoveMushrooms123'):
        return self.__client.post(
            'authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
