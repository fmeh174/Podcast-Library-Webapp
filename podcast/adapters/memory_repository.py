from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from podcast.adapters.repository import AbstractRepository, RepositoryException
from podcast.domainmodel.model import *
from podcast.adapters.datareader.csvdatareader import CSVDataReader


class MemoryRepository(AbstractRepository):
    #  ids all assumed unique.

    def __init__(self):
        self.__authors = list()
        self.__podcasts = list()
        self.__podcasts_index = dict()
        self.__categories = list()
        self.__categories_index = dict()
        self.__users = list()
        self.__users_index = dict()
        self.__subscriptions = list()
        self.__subscriptions_index = dict()
        self.__episodes = list()
        self.__episodes_index = dict()
        self.__reviews = list()
        self.__playlists = list()

    def add_author(self, author: Author):
        self.__authors.append(author)

    def get_author(self, author_name) -> Author:
        return next((author for author in self.__authors if author.name == author_name), None)

    def add_podcast(self, podcast: Podcast):
        if podcast not in self.__podcasts:
            if podcast.author is not None:
                podcast.author.add_podcast(podcast)
            insort_left(self.__podcasts, podcast)
            self.__podcasts_index[podcast.id] = podcast

    def get_podcast(self, podcast_id) -> Podcast:
        podcast = None
        for podcast in self.__podcasts:
            if podcast.id == int(podcast_id):
                return podcast
            else:
                podcast = None
        return podcast

    def get_number_of_podcasts(self) -> int:
        return len(self.__podcasts)

    def get_list_of_podcasts(self) -> List[Podcast]:
        return self.__podcasts

    def get_podcasts_by_id(self, id_list) -> List[Podcast]:
        # Remove ids in id_list that don't represent Podcast ids in the repository.
        existing_ids = [id for id in id_list if id in self.__podcasts_index]

        # Fetch for Podcasts.
        podcasts = [self.__podcasts_index[id] for id in existing_ids]
        return podcasts

    def get_podcast_ids_by_category(self, category_name: str):
        # Linear search to find the first occurrence of each Category with the name category_name
        category = next((category for category in self.__categories if category.name == category_name), None)

        # Retrieve the ids of Podcasts associated with the Category.
        if category is not None:
            podcast_ids = [podcast.id for podcast in self.__podcasts if category in podcast.categories]
        else:
            # No Category with name category_name, so return empty list.
            podcast_ids = list()

        return podcast_ids

    def get_podcast_ids_by_language(self, language: str):
        # Retrieve the ids of Podcasts with Language 'language'.
        podcast_ids = [podcast.id for podcast in self.__podcasts if podcast.language == language]
        return podcast_ids

    def add_category(self, category: Category):
        self.__categories.append(category)

    def get_categories(self):
        return self.__categories

    def add_user(self, user: User):
        if user not in self.__users:
            insort_left(self.__users, user)
            self.__users_index[user.id] = user

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.username.lower() == user_name.lower()), None)

    def get_number_of_users(self) -> int:
        return len(self.__users)

    def add_podcast_subscription(self, subscription: PodcastSubscription):
        subscription.owner.add_subscription(subscription)
        insort_left(self.__subscriptions, subscription)
        self.__subscriptions_index[subscription.id] = subscription

    def get_podcast_subscription(self, sub_id) -> PodcastSubscription:
        subscription = None

        try:
            subscription = self.__subscriptions_index[sub_id]
        except KeyError:
            pass  # Ignore the exception and return None.

        return subscription

    def add_episode(self, episode: Episode):
        parent = None
        try:
            parent = self.__podcasts_index[episode.podcast.id]
        except KeyError:
            pass
        except AttributeError:
            pass
        if parent is not None:
            parent.add_episode(episode)
            insort_left(self.__episodes, episode)
            self.__episodes_index[episode.id] = episode

    def get_episode(self, episode_id) -> Episode:
        for episode in self.__episodes:
            if episode.id == int(episode_id):
                return episode
        return None

    def get_number_of_episodes(self) -> int:
        return len(self.__episodes)

    def get_first_episode(self) -> Episode:
        episode = None

        if len(self.__episodes) > 0:
            episode = self.__episodes[0]
        return episode

    def get_last_episode(self) -> Episode:
        episode = None

        if len(self.__episodes) > 0:
            episode = self.__episodes[-1]
        return episode

    def get_episodes_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Episode ids in the repository.
        existing_ids = [id for id in id_list if id in self.__episodes_index]

        # Fetch the Episodes.
        episodes = [self.__episodes_index[id] for id in existing_ids]
        return episodes

    def get_next_episode_id(self, episode: Episode):
        next_id = None

        try:
            index = self.episode_index(episode)
            for stored_episode in self.__episodes[index + 1:len(self.__episodes)]:
                if stored_episode.id > episode.id:
                    next_id = stored_episode.id
                    break
        except ValueError:
            # No next Episode
            pass

        return next_id

    def get_previous_episode_id(self, episode: Episode):
        previous_id = None

        try:
            index = self.episode_index(episode)
            for stored_episode in reversed(self.__episodes[0:index]):
                if stored_episode.id < episode.id:
                    previous_id = stored_episode.id
                    break
        except ValueError:
            # No previous Episode
            pass

        return previous_id

    def add_review(self, review: Review):
        review.user.add_review(review)
        review.episode.add_review(review)
        self.__reviews.append(review)

    def get_reviews(self) -> List[Review]:
        return self.__reviews

    def get_number_of_reviews(self) -> int:
        return len(self.__reviews)

    def add_playlist(self, playlist: Playlist):
        playlist.owner.add_playlist(playlist)
        self.__playlists.append(playlist)

    def get_playlists(self) -> List[Playlist]:
        return self.__playlists

    # Helper method to return episode index.
    def episode_index(self, episode: Episode):
        index = bisect_left(self.__episodes, episode)
        if index != len(self.__episodes) and self.__episodes[index].id == episode.id:
            return index
        raise ValueError
