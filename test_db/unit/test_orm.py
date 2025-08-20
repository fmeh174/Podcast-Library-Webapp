import pytest
from datetime import datetime
from podcast.domainmodel.model import Author, Podcast, Episode, Category, User, Review, Playlist, make_review

@pytest.fixture
def user():
    return User(1, "jon", "password123")


@pytest.fixture
def podcast(author):
    return Podcast(1, author, "D-Hour Radio Network", description="test description", image="test url", website="test url website", itunes_id=123, language="english")


@pytest.fixture
def author():
    return Author(2, name="D Hour Radio Network")


@pytest.fixture
def episode(podcast):
    episode = Episode(1, podcast, "D-Hour Radio Network", episode_audio="test audio", episode_length=10, upload_date=datetime(2024, 1, 1))
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


def test_saving_and_loading_author(empty_session, author):
    """Test saving and loading an Author object."""
    empty_session.add(author)
    empty_session.commit()

    fetched_author = empty_session.query(Author).filter_by(_name="D Hour Radio Network").first()
    assert fetched_author._name == author._name


def test_saving_and_loading_podcast(empty_session, podcast):
    """Test saving and loading a Podcast object."""
    empty_session.add(podcast)
    empty_session.commit()

    fetched_podcast = empty_session.query(Podcast).filter_by(_title="D-Hour Radio Network").first()
    assert fetched_podcast._title == podcast._title
    assert fetched_podcast._author._name == podcast._author._name


def test_saving_and_loading_episode(empty_session, episode_2):
    """Test saving and loading an Episode object."""
    empty_session.add(episode_2)
    empty_session.commit()

    retrieved_episode = empty_session.query(Episode).filter_by(_title="Brian Denny Radio").first()
    assert retrieved_episode._title == episode_2._title
    assert retrieved_episode._podcast._title == episode_2._podcast._title


def test_saving_and_loading_category(empty_session):
    """Test saving and loading a Category object."""
    category = Category(1, name="Technology")
    empty_session.add(category)
    empty_session.commit()

    fetched_category = empty_session.query(Category).filter_by(_name="Technology").first()
    assert fetched_category._name == "Technology"


def test_relationship_podcast_category(empty_session, podcast):
    """Test the relationship between Podcast and Category."""
    category = Category(1, name="Technology")
    podcast.categories.append(category)
    empty_session.add(podcast)
    empty_session.commit()

    fetched_podcast = empty_session.query(Podcast).filter_by(_title="D-Hour Radio Network").first()
    assert len(fetched_podcast.categories) == 1
    assert fetched_podcast.categories[0]._name == "Technology"


def test_saving_and_loading_user(empty_session, user):
    """Test saving and loading a User object."""
    empty_session.add(user)
    empty_session.commit()

    fetched_user = empty_session.query(User).filter_by(_username="jon").first()
    assert fetched_user._username == "jon"
    assert fetched_user._password == "password123"


def test_relationship_user_review(empty_session, user, review):
    """Test the relationship between User and Review."""
    empty_session.add(review)
    empty_session.commit()

    fetched_review = empty_session.query(Review).filter_by(_content="Amazing episode!").first()
    assert fetched_review._user._username == "jon"
    assert fetched_review._episode._title == "D-Hour Radio Network"


def test_relationship_playlist_episode(empty_session, user, episode):
    """Test the relationship between Playlist and Episode."""
    playlist = Playlist(1, user, "My Playlist")
    playlist._episodes.append(episode)
    empty_session.add(playlist)
    empty_session.commit()

    retrieved_playlist = empty_session.query(Playlist).filter_by(_title="My Playlist").first()
    assert len(retrieved_playlist._episodes) == 1
    assert retrieved_playlist._episodes[0]._title == "D-Hour Radio Network"


def test_saving_and_loading_review(empty_session, review):
    """Test saving and loading a Review object."""
    empty_session.add(review)
    empty_session.commit()

    fetched_review = empty_session.query(Review).filter_by(_content="Amazing episode!").first()
    assert fetched_review._content == "Amazing episode!"
    assert fetched_review._user._username == "jon"
    assert fetched_review._episode._title == "D-Hour Radio Network"


def test_saving_playlist(empty_session, user, episode):
    """Test saving and loading a Playlist with associated Episodes."""
    playlist = Playlist(1, user, "Sample Playlist")
    playlist._episodes.append(episode)
    empty_session.add(playlist)
    empty_session.commit()

    fetched_playlist = empty_session.query(Playlist).filter_by(_title="Sample Playlist").first()
    assert fetched_playlist._title == "Sample Playlist"
    assert len(fetched_playlist._episodes) == 1
    assert fetched_playlist._episodes[0]._title == episode._title
