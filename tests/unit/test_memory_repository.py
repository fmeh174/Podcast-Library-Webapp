

import pytest

from podcast import MemoryRepository
from podcast.domainmodel.model import *
from podcast.adapters.repo_populate import populate
from path_utils.utils import get_project_root


@pytest.fixture
def empty_memory_repo():
    return MemoryRepository()


@pytest.fixture
def author():
    return Author(2, name= "D Hour Radio Network")


@pytest.fixture
def author_2():
    return Author(3, name="Brian Denny")


@pytest.fixture
def podcast(author):
    return Podcast(1, author, "D-Hour Radio Network")


@pytest.fixture
def podcast_2(author_2):
    return Podcast(2, author_2, "Brian Denny Radio")


@pytest.fixture
def category():
    return Category(1, "Society & Culture")


@pytest.fixture
def user():
    return User(1, "jon", "password123")


@pytest.fixture
def user_2():
    return User(2, "liam", "password1234")


@pytest.fixture
def episode(podcast):
    episode = Episode(1, podcast, "D-Hour Radio Network")
    return episode


@pytest.fixture
def episode_2(podcast):
    episode = Episode(2, podcast, "Brian Denny Radio")
    return episode


def test_add_and_get_author(in_memory_repo, author):
    retrieved_author = in_memory_repo.get_author("D Hour Radio Network")
    assert retrieved_author == author

    assert in_memory_repo.get_author("Diddy") is None
    author2 = Author(10, "Diddy")
    in_memory_repo.add_author(author2)
    retrieved_author2 = in_memory_repo.get_author("Diddy")
    assert retrieved_author2 == author2


def test_add_and_get_podcast(in_memory_repo, podcast):
    assert in_memory_repo.get_podcast(7) is None
    retrieved_podcast = in_memory_repo.get_podcast(1)
    assert retrieved_podcast == podcast


def test_get_number_of_podcasts(in_memory_repo, author, author_2, podcast_2):
    assert in_memory_repo.get_number_of_podcasts() == 7
    podcast2 = Podcast(10, author, "Test Podcast")
    in_memory_repo.add_podcast(podcast2)
    assert in_memory_repo.get_number_of_podcasts() == 8
    in_memory_repo.add_podcast(podcast_2)
    assert in_memory_repo.get_number_of_podcasts() == 8
    test_num = 60
    for i in range(test_num):
        pod_test = Podcast(i+20)
        in_memory_repo.add_podcast(pod_test)
    assert in_memory_repo.get_number_of_podcasts() == test_num + 8


def test_get_list_of_podcasts(empty_memory_repo, author, podcast, author_2, podcast_2):
    assert empty_memory_repo.get_list_of_podcasts() == []
    empty_memory_repo.add_podcast(podcast)
    assert empty_memory_repo.get_list_of_podcasts() == [podcast]
    empty_memory_repo.add_podcast(podcast_2)
    podcasts = empty_memory_repo.get_list_of_podcasts()
    assert podcast in podcasts
    assert podcast_2 in podcasts


def test_get_podcats_ids_by_category(in_memory_repo, category, podcast, podcast_2):
    podcast.add_category(category)
    assert category in in_memory_repo.get_categories()
    podcast_id = in_memory_repo.get_podcast_ids_by_category(category.name)
    assert podcast.id in podcast_id
    assert podcast_2.id not in podcast_id
    podcast_id = in_memory_repo.get_podcast_ids_by_category("None")
    assert len(podcast_id) == 0


def test_get_podcasts_by_language(in_memory_repo, podcast):
    podcast_3 = Podcast(10, title= "My Spanish Podcast", language="Spanish")
    in_memory_repo.add_podcast(podcast_3)
    english_ids = in_memory_repo.get_podcast_ids_by_language("English")
    spanish_ids = in_memory_repo.get_podcast_ids_by_language("Spanish")
    assert podcast.id in english_ids
    assert podcast_3.id in spanish_ids
    assert podcast.title not in spanish_ids
    assert podcast_3.title not in english_ids


def test_add_and_get_user(in_memory_repo, user, user_2):
    in_memory_repo.add_user(user)
    user_got = in_memory_repo.get_user("jon")
    assert user_got == user
    assert in_memory_repo.get_user("tom") is None   #checks random name to see if repo is working as intended
    assert user_got != user_2 #checks if get_user is working properly


def test_add_and_get_podcast_subscription(in_memory_repo, user_2, podcast, user, podcast_2):
    assert in_memory_repo.get_podcast_subscription(1) is None # checks to see if there are no subscriptions
    subs = PodcastSubscription(1, user, podcast)
    in_memory_repo.add_podcast_subscription(subs)
    get_subscription = in_memory_repo.get_podcast_subscription(1)  #get_subscription
    assert get_subscription == subs     #checks to see if get_subscription == subscription added
    assert in_memory_repo.get_podcast_subscription(2) is None  #checks to see only one subscription was added
    subs_2 = PodcastSubscription(2,user_2,podcast_2)
    in_memory_repo.add_podcast_subscription(subs_2)
    get_subscription_2 = in_memory_repo.get_podcast_subscription(2)
    assert get_subscription != subs_2
    assert get_subscription_2 != subs  #checks to see if we can make multiple podcasts without any errors or data clash


def test_add_and_get_episode(in_memory_repo, podcast, podcast_2, episode, episode_2):
    # Check if there are no episodes initially
    assert in_memory_repo.get_episode(2) is None  # Check if episode with ID 2 does not exist
    assert in_memory_repo.get_episode(3) is None  # Check if episode with ID 3 does not exist
    in_memory_repo.add_podcast(podcast)
    in_memory_repo.add_episode(episode)
    get_episode = in_memory_repo.get_episode(1)
    assert get_episode == episode  # Verify if the added episode is correctly retrieved
    assert in_memory_repo.get_episode(2) is None
    in_memory_repo.add_podcast(podcast_2)
    in_memory_repo.add_episode(episode_2)
    get_episode_2 = in_memory_repo.get_episode(2)
    assert get_episode_2 == episode_2  # Verify the second episode is retrieved correctly
    assert get_episode == episode  # Ensure episode 1 is still correctly retrieved
    assert get_episode_2 != episode  # Ensure episode 2 is not the same as episode 1


def test_get_number_of_episodes(empty_memory_repo, podcast, episode, episode_2):
    assert empty_memory_repo.get_number_of_episodes() == 0
    empty_memory_repo.add_podcast(podcast)
    empty_memory_repo.add_episode(episode)
    assert empty_memory_repo.get_number_of_episodes() == 1
    empty_memory_repo.add_episode(episode_2)
    assert empty_memory_repo.get_number_of_episodes() == 2   #makes episodes and adds them to memory repo then gets the number of episodes


def test_get_first_and_last_episodes(in_memory_repo, podcast, episode, episode_2):
    in_memory_repo.add_podcast(podcast)
    in_memory_repo.add_episode(episode)
    in_memory_repo.add_episode(episode_2)  #makes a podcast and adds 2 episodes and then checks if the first and last episodes we get from the method call are equal to the ones we created.
    assert in_memory_repo.get_first_episode(), in_memory_repo.get_last_episode() == (episode, episode_2)


def test_get_episodes_by_id(in_memory_repo, podcast, episode, episode_2):
    in_memory_repo.add_podcast(podcast)
    in_memory_repo.add_episode(episode)
    in_memory_repo.add_episode(episode_2)
    episodes_id = in_memory_repo.get_episodes_by_id([1,2])
    assert episode in episodes_id
    assert episode_2 in episodes_id #gets episodes from id list


def test_get_next_and_previous_episode_id(in_memory_repo, podcast, episode, episode_2):
    in_memory_repo.add_podcast(podcast)
    in_memory_repo.add_episode(episode)
    in_memory_repo.add_episode(episode_2)
    assert in_memory_repo.get_next_episode_id(episode) == 2
    assert in_memory_repo.get_next_episode_id(episode_2) is None
    assert in_memory_repo.get_previous_episode_id(episode_2) == 1
    assert in_memory_repo.get_previous_episode_id(episode) is None


def test_add_and_get_review(in_memory_repo, user, podcast, episode, episode_2, podcast_2, user_2):
    user_review_1 = Review(1, user, 10, "very good podcast", podcast, episode)
    in_memory_repo.add_review(user_review_1)
    user_review_2 = Review(2, user_2, 1, "would not recommend", podcast_2, episode_2)
    in_memory_repo.add_review(user_review_2)
    reviews = in_memory_repo.get_reviews()
    assert user_review_1 in reviews
    assert user_review_2 in reviews


def test_add_and_get_playlist(in_memory_repo, user):
    playlist = Playlist(1, user,"playlist 1")
    in_memory_repo.add_playlist(playlist)
    playlists = in_memory_repo.get_playlists()
    assert playlist in playlists


def test_populate(in_memory_repo):
    # Construct the path
    podcasts_file = get_project_root() / "podcast" / "adapters" / "data"
    # Initialize the repository
    # Populate the repository with data from the CSV files
    populate(podcasts_file, in_memory_repo)
    num_podcasts = in_memory_repo.get_number_of_podcasts()
    num_episodes = in_memory_repo.get_number_of_episodes()
    assert num_podcasts > 0, "No podcasts were loaded into the repository."
    assert num_episodes > 0, "No episodes were loaded into the repository."
