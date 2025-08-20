import abc
from typing import List
from datetime import date

from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist


repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_author(self, author: Author):
        raise NotImplementedError

    @abc.abstractmethod
    def get_author(self, author_name) -> Author:
        """ Returns Author named author_name from repository

        If there is no Author with such name, returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_podcast(self, podcast: Podcast):
        # Used to check for link to author object, no longer does as some podcasts are missing authors.
        # I.e. Row 293 and 295 in podcasts.csv
        """
        if podcast.author is None or podcast not in podcast.author.podcast_list:
            raise RepositoryException("Podcast not currently attached to an Author")
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast(self, podcast_id) -> Podcast:
        """ Returns Podcast with id podcast_id from repository.

        If there is no such Podcast with given id, returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_podcasts(self) -> int:
        """Returns the number of Podcasts in the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts_by_id(self, id_list) -> List[Podcast]:
        """ Returns a list of podcasts whose ids match those in id_list, from repo.

        If there are no matches, returns empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_list_of_podcasts(self) -> List[Podcast]:
        """Returns list of podcasts"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast_ids_by_category(self, category_name: str):
        """ Returns a list of ids representing Podcasts tagged by category_name

        If there are no Podcasts tagged by category_name, returns empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast_ids_by_language(self, language: str):
        """ Returns a list of ids representing Podcasts with the given langauge

        If there are no Podcasts of the given language, returns empty list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_category(self, category: Category):
        raise NotImplementedError

    @abc.abstractmethod
    def get_categories(self) -> List[Category]:
        """ Returns the Categories stored in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_users(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def add_podcast_subscription(self, subscription: PodcastSubscription):
        """ Adds a PodcastScubscription to the repository.

        If the PodcastSubscription doesn't have a link with a User,
        this method raises a RepositoryException and doesn't update the repository.
        """
        #  May want to make bidirectional link with Podcast class,
        #  would need to add a _subscriptions attribute to Podcast.
        if subscription.owner is None or subscription not in subscription.owner.subscription_list:
            raise RepositoryException("Subscription not currently attached to a User")
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast_subscription(self, sub_id) -> PodcastSubscription:
        """ Gets a PodcastSubscription from the repository.

        If there is no PodcastSubscription with the id sub_id, returns None. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_episode(self, episode: Episode):
        """ Adds an Episode to the repository. """

        #  MAY WANT TO IMPLEMENT THE FOLLOWING:
        #  If the Episode doesn't have a link to a Podcast,
        #  this method raises a RepositoryException and doesn't update the repository.
        raise NotImplementedError

    @abc.abstractmethod
    def get_episode(self, episode_id) -> Episode:
        """ Returns Episode with corresponding episode_id from repository.

        If there is no such episode, returns None"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_episodes(self) -> int:
        """ Returns the number of episodes in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_episode(self) -> Episode:
        """ Returns the first episode, ordered by date, from the repository.

        Returns None if repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_episode(self) -> Episode:
        """ Returns the last episode, ordered by date, from the repository.

        Returns None if repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes_by_id(self, id_list):
        """ Returns a list of Episodes whose ids match those in id_list, from the repository.

        If there are no matches, returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_episode_id(self, episode: Episode):
        """ Returns the next Episode, decided by date, from the current Podcast.

        Returns None if there is no next episode.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_previous_episode_id(self, episode: Episode):
        """ Returns the previous Episode, decided by date, from the current Podcast.

        Returns None if there is no previous episode.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds Review to the repository .

        If the Review doesn't have bidirectional links with an Episode and a User,
        this method raises a RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException("Review not currently attached to a User")
        if review.episode is None or review not in review.episode.reviews:
            raise RepositoryException("Review not currently attached to an Episode")
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self) -> List[Review]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_reviews(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def add_playlist(self, playlist: Playlist):
        """ Adds playlist to the repository.

        If the playlist doesn't have a link to a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if playlist.owner is None or playlist not in playlist.owner.playlists:
            raise RepositoryException("playlist not currently attached to a User")
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlists(self) -> List[Playlist]:
        raise NotImplementedError
