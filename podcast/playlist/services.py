from podcast import MemoryRepository
from podcast.domainmodel.model import Podcast, Review, Episode, make_review, Playlist, User
from podcast.adapters.repository import AbstractRepository


def get_user(repo: AbstractRepository, username: str):
    return repo.get_user(username)


def get_episode(repo: AbstractRepository, episode_id) -> Episode:
    return repo.get_episode(episode_id)


def get_podcast(repo: AbstractRepository, podcast_id: str) -> Podcast:
    return repo.get_podcast(podcast_id)
