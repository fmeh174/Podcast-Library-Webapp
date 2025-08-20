

import pytest

from podcast.domainmodel.model import *
from podcast.episodes import services


@pytest.fixture
def user():
    return User(1, "jon", "password123")


@pytest.fixture
def podcast(author):
    return Podcast(1, author, "D-Hour Radio Network", description="test description", image="test url", website="test url website", itunes_id=123, language= "english")


@pytest.fixture
def author():
    return Author(2, name= "D Hour Radio Network")


@pytest.fixture
def episode(podcast):
    episode = Episode(1, podcast, "D-Hour Radio Network", episode_audio="test audio", episode_length= 10, upload_date= datetime(2024, 1, 1))
    return episode


@pytest.fixture
def episode_2(podcast):
    episode = Episode(2, podcast, "Brian Denny Radio", episode_audio="test audio 2", episode_length=15, upload_date=datetime(2024, 1, 2))
    return episode


@pytest.fixture
def review(user, podcast, episode):
    return Review(1, user, 5, "Amazing episode!", podcast, episode, post_date=datetime(2024, 1, 1))


@pytest.fixture
def review2(user, podcast, episode):
    return Review(2, user, 3, "Good episode, but could be better.", podcast, episode, post_date=datetime(2024, 1, 2))


def test_add_review(in_memory_repo, podcast, episode, user):
    # Add the podcast, episode, and user to the repository
    in_memory_repo.add_podcast(podcast)
    in_memory_repo.add_episode(episode)
    in_memory_repo.add_user(user)

    # Add the first review
    services.add_review(podcast.id, episode.id, "Amazing episode!", user.username, 5, in_memory_repo)

    # Add the second review
    services.add_review(podcast.id, episode.id, "Great episode!", user.username, 4, in_memory_repo)

    # Assert that both reviews were added
    reviews = in_memory_repo.get_reviews()

    # Check the total number of reviews
    assert len(reviews) == 2

    # Check the content and details of the first review
    assert reviews[0].content == "Amazing episode!"
    assert reviews[0].user.username == user.username
    assert reviews[0].podcast.id == podcast.id
    assert reviews[0].episode.id == episode.id

    # Check the content and details of the second review
    assert reviews[1].content == "Great episode!"
    assert reviews[1].user.username == user.username
    assert reviews[1].podcast.id == podcast.id
    assert reviews[1].episode.id == episode.id


def test_get_reviews_for_episode(in_memory_repo, episode, review):
    # Add episode and review to the repository
    in_memory_repo.add_episode(episode)
    in_memory_repo.add_review(review)

    # Fetch reviews for the episode
    reviews = services.get_reviews_for_episode(episode.id, in_memory_repo)

    # Assert the correct reviews are returned
    assert len(reviews) == 1
    assert reviews[0]['content'] == review.content
    assert reviews[0]['rating'] == review.user_rating
    assert reviews[0]['episode_id'] == episode.id


def test_get_episode(in_memory_repo, episode):
    # Add episode to the repository
    in_memory_repo.add_episode(episode)

    # Fetch the episode
    episode_data = services.get_episode(episode.id, in_memory_repo)

    # Assert the correct episode data is returned
    assert episode_data['id'] == episode.id
    assert episode_data['title'] == episode.title
    #episode is turned into a dict so we can check if the key == the episode values


def test_review_to_dict(review):
    # Convert the review to a dictionary
    review_dict = services.review_to_dict(review)

    # Assert the correct values are in the dictionary
    assert review_dict['review_id'] == review.id
    assert review_dict['user_name'] == review.user.username
    assert review_dict['rating'] == review.user_rating
    assert review_dict['content'] == review.content
    assert review_dict['podcast_id'] == review.podcast.id
    assert review_dict['episode_id'] == review.episode.id
    assert review_dict['timestamp'] == review.post_date


def test_reviews_to_dict(review, review2):
    # Create a list of reviews
    reviews = [review, review2]  # Two distinct reviews
    reviews_dict = services.reviews_to_dict(reviews)

    # Assert both reviews were converted to dictionaries
    assert len(reviews_dict) == 2

    # Check the first review
    assert reviews_dict[0]['review_id'] == review.id
    assert reviews_dict[0]['user_name'] == review.user.username
    assert reviews_dict[0]['rating'] == review.user_rating
    assert reviews_dict[0]['content'] == review.content
    assert reviews_dict[0]['podcast_id'] == review.podcast.id
    assert reviews_dict[0]['episode_id'] == review.episode.id
    assert reviews_dict[0]['timestamp'] == review.post_date

    # Check the second review
    assert reviews_dict[1]['review_id'] == review2.id
    assert reviews_dict[1]['user_name'] == review2.user.username
    assert reviews_dict[1]['rating'] == review2.user_rating
    assert reviews_dict[1]['content'] == review2.content
    assert reviews_dict[1]['podcast_id'] == review2.podcast.id
    assert reviews_dict[1]['episode_id'] == review2.episode.id
    assert reviews_dict[1]['timestamp'] == review2.post_date


def test_episode_to_dict(episode, podcast, review):
    # Add a review to the episode
    episode.reviews.append(review)

    # Convert the episode to a dictionary
    episode_dict = services.episode_to_dict(episode)

    # Assert the correct values are in the dictionary
    assert episode_dict['id'] == episode.id
    assert episode_dict['podcast_id'] == episode.podcast.id
    assert episode_dict['title'] == episode.title
    assert episode_dict['audio'] == episode.audio
#    assert episode_dict['length'] == episode.length
    assert episode_dict['description'] == episode.description
    assert episode_dict['upload_date'] == episode.upload_date

    # Check the reviews in the episode
    #assert len(episode_dict['reviews']) == 1
    assert episode_dict['reviews'][0]['content'] == review.content


def test_episodes_to_dict(episode, episode_2):
    episodes = [episode, episode_2]
    episodes_dict = services.episodes_to_dict(episodes)

    assert len(episodes_dict) == 2

    # Check first episode
    assert episodes_dict[0]['id'] == episode.id
    assert episodes_dict[0]['title'] == episode.title
    assert episodes_dict[0]['audio'] == episode.audio
#   assert episodes_dict[0]['length'] == episode.length
    assert episodes_dict[0]['upload_date'] == episode.upload_date

    # Check second episode
    assert episodes_dict[1]['id'] == episode_2.id
    assert episodes_dict[1]['title'] == episode_2.title
    assert episodes_dict[1]['audio'] == episode_2.audio
#    assert episodes_dict[1]['length'] == episode_2.length
    assert episodes_dict[1]['upload_date'] == episode_2.upload_date


def test_get_user(in_memory_repo, user):
    # Add the user to the repository
    in_memory_repo.add_user(user)

    # Retrieve the user
    retrieved_user = services.get_user(in_memory_repo, user.username)

    # Assert that the correct user is retrieved
    assert retrieved_user is not None
    assert retrieved_user.username == user.username
    assert retrieved_user.id == user.id
    assert retrieved_user == user
