from typing import Iterable

from podcast.adapters.memory_repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Review, Episode, make_review


class NonExistentPodcastException(Exception):
    pass


class NonExistentEpisodeException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(podcast_id: int, episode_id: int, review_text: str, user_name: str, rating: int, repo: AbstractRepository):
    # Check that the podcast exists
    podcast = repo.get_podcast(podcast_id)
    if podcast is None:
        raise NonExistentPodcastException

    episode = repo.get_episode(episode_id)
    if episode is None:
        raise NonExistentEpisodeException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    review_id = repo.get_number_of_reviews()

    # Create review
    review = make_review(review_id, review_text, user, podcast, episode, rating)

    # Update repository
    repo.add_review(review)


def get_reviews_for_episode(episode_id: int, repo: AbstractRepository):
    episode = repo.get_episode(episode_id)

    if episode is None:
        raise NonExistentEpisodeException

    return reviews_to_dict(episode.reviews)


def get_episode(episode_id: int, repo: AbstractRepository):
    episode = repo.get_episode(episode_id)

    if episode is None:
        raise NonExistentEpisodeException

    return episode_to_dict(episode)


def review_to_dict(review: Review):
    review_dict = {
        'review_id': review.id,
        'user_name': review.user.username,
        'rating': review.user_rating,
        'content': review.content,
        'podcast_id': review.podcast.id,
        'episode_id': review.episode.id,
        'timestamp': review.post_date
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def episode_to_dict(episode: Episode):
    episode_dict = {
        'id': episode.id,
        'podcast_id': episode.podcast.id,
        'title': episode.title,
        'audio': episode.audio,
        'description': episode.description,
        'upload_date': episode.upload_date,
        'reviews': reviews_to_dict(episode.reviews)
    }
    return episode_dict


def episodes_to_dict(episodes: Iterable[Episode]):
    return [episode_to_dict(episode) for episode in episodes]


def get_user(repo: AbstractRepository, username: str):
    return repo.get_user(username)
