from datetime import date

import pytest

from podcast.authentication import services as auth_services
from podcast.episodes import services as episode_services
from podcast.episodes.services import NonExistentEpisodeException, NonExistentPodcastException


def test_can_add_review(in_memory_repo):
    podcast_id = 14
    episode_id = 1
    review_text = "I'm placing blocks and shit 'cause I'm in fuckin' Minecraft!"
    user_name = "JBlack"

    auth_services.add_user(user_name, "Minecraft123", in_memory_repo)

    # Call the service layer to add the review
    episode_services.add_review(podcast_id, episode_id, review_text, user_name, 5, in_memory_repo)

    # Retrieve reviews for the episode from the repository
    comments_as_dict = episode_services.get_reviews_for_episode(episode_id, in_memory_repo)

    # Check that the reviews includes the added review
    assert next(
        (dictionary['content'] for dictionary in comments_as_dict if dictionary['content'] == review_text),
        None) is not None


def test_cannot_add_review_for_nonexistent_podcast(in_memory_repo):
    podcast_id = 100
    episode_id = 100
    review_text = "BLEGH"
    user_name = "JBlack"

    with pytest.raises(NonExistentPodcastException):
        episode_services.add_review(podcast_id, episode_id, review_text, user_name, 5, in_memory_repo)


def test_cannot_add_review_for_unknown_user(in_memory_repo):
    podcast_id = 14
    episode_id = 1
    review_text = "Wasn't very good."
    user_name = "Dunkey"

    with pytest.raises(episode_services.UnknownUserException):
        episode_services.add_review(podcast_id, episode_id, review_text, user_name, 1, in_memory_repo)
