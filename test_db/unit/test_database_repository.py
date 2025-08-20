import pytest

from podcast import SqlAlchemyRepository
from podcast.domainmodel.model import Author, Podcast, User, Episode, Review, Playlist, Category


def test_repository_can_add_and_get_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    author = Author(1, 'Diddy')
    repo.add_author(author)

    retrieved_author = repo.get_author('Diddy')
    assert retrieved_author == author


def test_repository_returns_none_for_non_existent_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    author = repo.get_author('Jane Doe')
    assert author is None


def test_repository_can_add_and_get_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    author = Author(1, 'Podcast Author')
    podcast = Podcast(1, author, 'Sample Podcast', description='A sample podcast description')

    repo.add_podcast(podcast)

    retrieved_podcast = repo.get_podcast(1)
    assert retrieved_podcast == podcast


def test_repository_returns_none_for_non_existent_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcast = repo.get_podcast(999)
    assert podcast is None


def test_repository_can_add_and_get_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'user1', 'password123')
    repo.add_user(user)

    retrieved_user = repo.get_user('user1')
    assert retrieved_user == user


def test_repository_can_add_and_get_episode(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    author = Author(1, 'Author Name')
    podcast = Podcast(1, author, 'Sample Podcast')
    episode = Episode(1, podcast, 'Sample Episode')

    repo.add_episode(episode)

    retrieved_episode = repo.get_episode(1)
    assert retrieved_episode == episode


def test_repository_can_add_and_get_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'user1', 'password123')
    author = Author(1, 'Author Name')
    podcast = Podcast(1, author, 'Sample Podcast')
    episode = Episode(1, podcast, 'Sample Episode')
    review = Review(1, user, 5, 'Great episode!', podcast, episode)

    repo.add_review(review)

    retrieved_reviews = repo.get_reviews()
    assert len(retrieved_reviews) == 1
    assert retrieved_reviews[0] == review


def test_repository_can_add_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'user1', 'password123')
    playlist = Playlist(1, user, "My playlist")

    repo.add_playlist(playlist)

    playlists = repo.get_playlists()
    assert len(playlists) == 1
    assert playlists[0] == playlist


def test_repository_can_add_and_remove_episode_from_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'user1', 'password123')
    playlist = Playlist(1, user, "My playlist")
    episode = Episode(1, Podcast(1, Author(1, 'Author Name'), 'Sample Podcast'), 'Sample Episode')

    repo.add_playlist(playlist)
    repo.add_episode_to_playlist(user, episode)

    # Check if episode is added
    playlists = repo.get_playlists()
    assert episode in playlists[0].episodes

    # Remove episode
    repo.remove_episode_from_playlist(user, episode)
    assert episode not in playlists[0].episodes


def test_repository_can_retrieve_number_of_podcasts(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    author = Author(1, 'Podcast Author')
    podcast1 = Podcast(1, author, 'Sample Podcast 1')
    podcast2 = Podcast(2, author, 'Sample Podcast 2')

    repo.add_podcast(podcast1)
    repo.add_podcast(podcast2)

    number_of_podcasts = repo.get_number_of_podcasts()
    assert number_of_podcasts == 2


def test_repository_can_get_podcast_ids_by_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    category = Category(1, 'Tech')
    author = Author(1, 'Author Name')
    podcast = Podcast(1, author, 'Tech Podcast')
    podcast.add_category(category)

    repo.add_category(category)
    repo.add_podcast(podcast)

    podcast_ids = repo.get_podcast_ids_by_category('Tech')
    assert len(podcast_ids) == 1
    assert podcast_ids[0] == 1


def test_repository_can_add_and_get_podcast_by_language(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    author = Author(1, 'Podcast Author')
    podcast = Podcast(1, author, 'Sample Podcast', language='English')

    repo.add_podcast(podcast)

    podcasts = repo.get_podcast_ids_by_language('English')
    assert len(podcasts) == 1
    assert podcasts[0] == podcast


def test_repository_can_get_number_of_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'user1', 'password123')
    author = Author(1, 'Author Name')
    podcast = Podcast(1, author, 'Sample Podcast')
    episode = Episode(1, podcast, 'Sample Episode')
    review = Review(1, user, 5, 'Great episode!', podcast, episode)

    repo.add_review(review)

    number_of_reviews = repo.get_number_of_reviews()
    assert number_of_reviews == 1