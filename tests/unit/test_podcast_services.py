

import pytest

from podcast import MemoryRepository
from podcast.domainmodel.model import *
from podcast.podcasts import services


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
    return Podcast(1, author, "D-Hour Radio Network", "test url", "test description", "test url website", 123, "english")


@pytest.fixture
def podcast_2(author_2):
    return Podcast(2, author_2, "Brian Denny Radio")


@pytest.fixture
def category():
    return Category(1, "Society & Culture")


@pytest.fixture
def category_2():
    return Category(2, "Rock and roll")


@pytest.fixture
def user():
    return User(1, "jon", "password123")


@pytest.fixture
def user_2():
    return User(2, "liam", "password1234")


@pytest.fixture
def episode(podcast):
    episode = Episode(1, podcast, "D-Hour Radio Network", episode_audio="test audio", episode_length= 10, episode_desc="test description", upload_date= datetime(2024, 1, 1))
    return episode


@pytest.fixture
def episode_2(podcast):
    episode = Episode(2, podcast, "Brian Denny Radio")
    return episode


# Test cases
def test_get_number_of_podcasts(empty_memory_repo, podcast, podcast_2):
    assert empty_memory_repo.get_number_of_podcasts() == 0
    empty_memory_repo.add_podcast(podcast)
    assert services.get_number_of_podcasts(empty_memory_repo) == 1
    empty_memory_repo.add_podcast(podcast_2)
    assert services.get_number_of_podcasts(empty_memory_repo) == 2


def test_podcast_id(empty_memory_repo, podcast, podcast_2):
    empty_memory_repo.add_podcast(podcast)
    empty_memory_repo.add_podcast(podcast_2)
    first_podcast = services.podcast_id(1, empty_memory_repo)
    second_podcast = services.podcast_id(2, empty_memory_repo)
    print(empty_memory_repo.get_list_of_podcasts())
    assert first_podcast == services.podcast_to_dict(podcast)  #checks if the first_podcast returned is == podcast_to_dict(podcast) as first_podcast is now a dict
    assert second_podcast == services.podcast_to_dict(podcast_2) #checks if the second_podcast returned is == podcast_to_dict(podcast) as second_podcast is now a dict


def test_podcast_to_dict(empty_memory_repo, podcast, author, episode, episode_2):
    episode_list = [episode, episode_2]
    podcast.add_episode(episode)
    podcast.add_episode(episode_2)
    test_cata = Category(1, "Society & Culture")
    podcast.add_category(test_cata)
    dict_pod = services.podcast_to_dict(podcast)
    assert dict_pod["id"] == 1
    assert dict_pod["title"] == "D-Hour Radio Network"
    assert dict_pod["description"] == "test description"
    assert dict_pod["image"] == "test url"
    assert dict_pod["website"] == "test url website"
    assert dict_pod["itunes_id"] == 123
    assert dict_pod["language"] == "english"
    assert dict_pod["author"] == author
    assert dict_pod["categories"] == "Society & Culture"
    assert dict_pod["episodes"] == services.episodes_to_dict(episode_list)


def test_get_podcast_dicts(empty_memory_repo, podcast, author, podcast_2):
    empty_memory_repo.add_podcast(podcast)
    empty_memory_repo.add_podcast(podcast_2)
    dict_pod = services.podcast_to_dict(podcast)  #first dict in dict of podcasts
    dict_pod_2 = services.podcast_to_dict(podcast_2) #second dict
    podcast_dict = services.get_podcast_dicts(empty_memory_repo)
    assert podcast_dict[dict_pod["id"]] == dict_pod  #checks if dict_pod is in dict
    assert podcast_dict[dict_pod_2["id"]] == dict_pod_2  #checks if dict_pod_2 is in dict


def test_category_to_dict(empty_memory_repo, category, podcast, podcast_2):
    podcast.add_category(Category(1, "Society & Culture"))
    category.add_podcast(podcast)
    dict_cate = services.category_to_dict(category)
    assert dict_cate["id"] == 1
    assert dict_cate["name"] == "Society & Culture"
    empty_memory_repo.add_category(Category(1, "Society & Culture"))


def test_categories_to_dict(empty_memory_repo, category, podcast, podcast_2, category_2):
    list_of_categories = [category, category_2]
    cata_dict = services.categories_to_dict(list_of_categories) #dict of categories
    assert cata_dict[0] == services.category_to_dict(category)
    assert cata_dict[1] == services.category_to_dict(category_2)


def test_categories_to_string(empty_memory_repo, category, category_2):
    list_of_categories = [category, category_2]
    string_cata = services.categories_to_string(list_of_categories)
    assert string_cata == "Society & Culture | Rock and roll"


def test_episode_to_dict(empty_memory_repo, episode, user, podcast):
    empty_memory_repo.add_podcast(podcast)
    empty_memory_repo.add_episode(episode)
    user_review = Review(1, user, 10, "very good", podcast=podcast, episode=episode)
    episode.add_review(user_review)
    dict_episode = services.episode_to_dict(episode)
    assert dict_episode["id"] == 1
    assert dict_episode["title"] == "D-Hour Radio Network"
    assert dict_episode["podcast_id"] == 1
    assert dict_episode["description"] == "test description"
    assert dict_episode["audio"] == "test audio"
    assert dict_episode["upload_date"] == datetime(2024, 1, 1)
    assert dict_episode["reviews"] == [{'content': 'very good',
                                          'episode_id': 1,
                                          'podcast_id': podcast.id,
                                          'rating': 10,
                                          'review_id': 1,
                                          'timestamp': datetime(1970, 1, 1, 0, 0),
                                          'user_name': 'jon'}]


def test_episodes_to_dict(empty_memory_repo, episode, user, podcast, episode_2):
    episode_list = [episode, episode_2]
    episode_dict = services.episodes_to_dict(episode_list)
    assert episode_dict[0] == services.episode_to_dict(episode)
    assert episode_dict[1] == services.episode_to_dict(episode_2)


