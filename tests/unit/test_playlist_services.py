
import pytest
from podcast import MemoryRepository
from podcast.domainmodel.model import *


@pytest.fixture
def empty_memory_repo():
    return MemoryRepository()


@pytest.fixture
def podcast(author):
    return Podcast(1, author, "D-Hour Radio Network", description="test description", image="test url", website="test url website", itunes_id=123, language= "english")


@pytest.fixture
def user():
    return User(1, "jon", "password123")


@pytest.fixture
def episode(podcast):
    episode = Episode(1, podcast, "D-Hour Radio Network", episode_audio="test audio", episode_length= 10, upload_date= datetime(2024, 1, 1))
    return episode


@pytest.fixture
def author():
    return Author(2, name= "D Hour Radio Network")


def test_get_user(empty_memory_repo: MemoryRepository, user: User):
    # Add the user to the repository
    empty_memory_repo.add_user(user)

    # Now, call the function to get the user by username
    retrieved_user = empty_memory_repo.get_user(user.username)

    # Assert that the correct user is returned
    assert retrieved_user is not None
    assert isinstance(retrieved_user, User)
    assert retrieved_user.username == user.username

def test_get_episode(in_memory_repo, episode: Episode):
    # Add the episode to the repository
    in_memory_repo.add_episode(episode)
    # Now, call the function to get the episode by ID
    assert in_memory_repo.get_number_of_episodes() == 2
    retrieved_episode = in_memory_repo.get_episode(episode.id)

    # Assert that the correct episode is returned
    assert retrieved_episode is not None
    assert isinstance(retrieved_episode, Episode)
    assert retrieved_episode.id == episode.id
    assert retrieved_episode.title == episode.title
    assert retrieved_episode.audio == episode.audio


def test_get_podcast(in_memory_repo, podcast: Podcast):
    # Add the podcast to the repository
    in_memory_repo.add_podcast(podcast)

    # Now, call the function to get the podcast by ID
    retrieved_podcast = in_memory_repo.get_podcast(podcast.id)

    # Assert that the correct podcast is returned
    assert retrieved_podcast is not None
    assert isinstance(retrieved_podcast, Podcast)
    assert retrieved_podcast.id == podcast.id
    assert retrieved_podcast.title == podcast.title
    assert retrieved_podcast.author == podcast.author
