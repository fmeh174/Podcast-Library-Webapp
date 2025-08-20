from __future__ import annotations
import random
from datetime import datetime
from typing import List, Iterable
from flask import current_app


def validate_non_negative_int(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"ID: '{value}' must be a non-negative integer.")


def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


def validate_datetime_object(object, field_name="value"):
    if not isinstance(object, datetime):
        raise ValueError(f"{field_name} must be a datetime object")


class Author:
    def __init__(self, author_id: int, name: str):
        if author_id is not None:
            validate_non_negative_int(author_id)
        validate_non_empty_string(name, "Author name")
        self._id = author_id
        self._name = name.strip()
        self.podcast_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.podcast_list:
            self.podcast_list.append(podcast)

    def remove_podcast(self, podcast: Podcast):
        if podcast in self.podcast_list:
            self.podcast_list.remove(podcast)

    def __repr__(self) -> str:
        return f"<Author {self._id}: {self._name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.id == other.id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.id)


class Podcast:
    def __init__(self, podcast_id: int, author: Author = None, title: str = "Untitled", image: str = None,
                 description: str = "", website: str = "", itunes_id: int = None, language: str = "Unspecified"):
        validate_non_negative_int(podcast_id)
        self._id = podcast_id
        self._author = author
        validate_non_empty_string(title, "Podcast title")
        self._title = title.strip()
        self._image = image
        self._description = description
        self._language = language
        self._website = website
        self._itunes_id = itunes_id
        self.categories = []
        self.episodes = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def author(self) -> Author:
        return self._author

    @property
    def itunes_id(self) -> int:
        return self._itunes_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Podcast title")
        self._title = new_title.strip()

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_image: str):
        if new_image is not None and not isinstance(new_image, str):
            raise TypeError("Podcast image must be a string or None.")
        self._image = new_image

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Podcast description")
        self._description = new_description

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        if not isinstance(new_language, str):
            raise TypeError("Podcast language must be a string.")
        self._language = new_language

    @property
    def website(self) -> str:
        return self._website

    @website.setter
    def website(self, new_website: str):
        validate_non_empty_string(new_website, "Podcast website")
        self._website = new_website

    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance.")
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category: Category):
        if category in self.categories:
            self.categories.remove(category)

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self.episodes:
            self.episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self.episodes:
            self.episodes.remove(episode)
    #new
    def podcast_episodes(self, podcast: Podcast):
        return podcast.episodes

    def __repr__(self):
        return f"<Podcast {self.id}: '{self.title}' by {self.author.name}>"

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.title < other.title

    def __hash__(self):
        return hash(self.id)


class Category:
    def __init__(self, category_id: int, name: str):
        validate_non_negative_int(category_id)
        validate_non_empty_string(name, "Category name")
        self._id = category_id
        self._name = name.strip()
        self._tagged_podcasts = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    @property
    def tagged_podcasts(self) -> Iterable[Podcast]:
        return iter(self._tagged_podcasts)

    @property
    def number_of_tagged_podcasts(self) -> int:
        return len(self._tagged_podcasts)

    def is_applied_to(self, podcast: Podcast) -> bool:
        return podcast in self._tagged_podcasts

    def add_podcast(self, podcast: Podcast):
        self._tagged_podcasts.append(podcast)

    def __repr__(self) -> str:
        return f"<Category {self._id}: {self._name}>"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Category):
            return False
        return self._name < other.name

    def __hash__(self):
        return hash(self._id)


class User:
    def __init__(self, user_id: int, username: str, password: str):
        validate_non_negative_int(user_id)
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        self._id = user_id
        self._username = username.lower().strip()
        self._password = password
        self._subscription_list = []
        self._reviews = []
        self._playlists = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def subscription_list(self):
        return self._subscription_list

    def add_subscription(self, subscription: PodcastSubscription):
        if not isinstance(subscription, PodcastSubscription):
            raise TypeError("Subscription must be a PodcastSubscription object.")
        if subscription not in self._subscription_list:
            self._subscription_list.append(subscription)

    def remove_subscription(self, subscription: PodcastSubscription):
        if subscription in self._subscription_list:
            self._subscription_list.remove(subscription)

    @property
    def reviews(self):
        return self._reviews

    def add_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Review must be a Review object.")
        if review not in self._reviews:
            self._reviews.append(review)

    def remove_review(self, review: Review):
        if review in self._reviews:
            self._reviews.remove(review)

    @property
    def playlists(self):
        return self._playlists

    def add_playlist(self, playlist: Playlist):
        if not isinstance(playlist, Playlist):
            raise TypeError("Review must be a Review object.")
        if playlist not in self._playlists:
            self._playlists.append(playlist)

    #new
    def add_episode_to_playlist(self, episode: Episode):
        self._playlists.insert(0, episode)

    #new
    def remove_episode_from_playlist(self, episode: Episode):
        self._playlists.remove(episode)

    def remove_playlist(self, playlist: Playlist):
        if playlist in self._playlists:
            self._playlists.remove(playlist)

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class PodcastSubscription:
    def __init__(self, sub_id: int, owner: User, podcast: Podcast):
        validate_non_negative_int(sub_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = sub_id
        self._owner = owner
        self._podcast = podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    def __repr__(self):
        return f"<PodcastSubscription {self.id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id == other.id and self.owner == other.owner and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))


class Episode:
    def __init__(self, episode_id: int, podcast: Podcast, episode_title: str = "Untitled", episode_audio: str = "No link",
                 episode_length: int = 0, episode_desc: str = "No description", upload_date: datetime = datetime(1970, 1, 1)):
        validate_non_negative_int(episode_id)
        self._id = episode_id
        self._podcast = podcast
        validate_non_empty_string(episode_title, "Episode title")
        self._title = episode_title.strip()
        # No longer validates non-empty string for audio link; i.e. rows 171 and 172 in episode.csv having no audio.
        self._audio = episode_audio.strip()
        validate_non_negative_int(episode_length)
        self._length = episode_length
        # No longer validates non-empty string; i.e. row 43 in episodes.csv having no description.
        self._description = episode_desc.strip()
        validate_datetime_object(upload_date, "Upload date")
        self._upload_date = upload_date
        self._reviews = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def podcast(self):
        return self._podcast

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "New episode title")
        self._title = new_title.strip()

    @property
    def audio(self) -> str:
        return self._audio

    @audio.setter
    def audio(self, new_audio: str):
        validate_non_empty_string(new_audio, "New episode audio link")
        self._audio = new_audio.strip()

    @property
    def length(self) -> int:
        return self._length

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_desc):
        validate_non_empty_string(new_desc, "New episode description")
        self._description = new_desc.strip()

    @property
    def upload_date(self) -> datetime:
        return self._upload_date

    @property
    def reviews(self):
        return self._reviews

    def add_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Review must be a Review object.")
        if review not in self._reviews:
            self._reviews.append(review)

    def remove_review(self, review: Review):
        if review in self._reviews:
            self._reviews.remove(review)

    def __repr__(self):
        return f"<Episode {self._id}: '{self._title}' from podcast {self._podcast.id}>"

    def __eq__(self, other):
        if not isinstance(other, Episode):
            return False
        return self._id == other._id

    def __lt__(self, other):
        if not isinstance(other, Episode):
            return False
        return self._id < other._id

    def __gt__(self, other):
        if not isinstance(other, Episode):
            return False
        return self._id > other._id

    def __hash__(self):
        return hash((self.id, self.podcast.id, self.upload_date))


class Review:
    def __init__(self, review_id: int, user: User, rating: int, content: str,
                 podcast: Podcast = None, episode: Episode = None,
                 post_date: datetime = datetime(1970, 1, 1)):
        validate_non_negative_int(review_id)
        validate_non_empty_string(content)
        if not isinstance(user, User):
            raise TypeError("User must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        if not isinstance(episode, Episode):
            raise TypeError("Episode must be a Episode object.")
        self._id = review_id
        if podcast is None and episode is None:
            raise ValueError("A podcast or episode must be provided")
        self._podcast = podcast
        self._episode = episode
        self._user = user
        if (1 > rating > 5):
            raise ValueError("Rating must be between 1 and 5")
        self._user_rating = rating
        self._content = content
        self._post_date = post_date

    @property
    def id(self) -> int:
        return self._id

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @property
    def user(self) -> User:
        return self._user

    @property
    def user_rating(self) -> int:
        return self._user_rating

    @property
    def content(self) -> str:
        return self._content

    @property
    def episode(self) -> Episode:
        return self._episode

    @property
    def post_date(self) -> datetime:
        return self._post_date

    @content.setter
    def content(self, new_content: str):
        validate_non_empty_string(new_content, "New content")
        self._content = new_content.strip()

    @episode.setter
    def episode(self, new_episode: Episode):
        if not isinstance(new_episode, Episode):
            raise TypeError("Episode must be a Episode object.")
        self._episode = new_episode

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    @user_rating.setter
    def user_rating(self, new_rating: float):
        if (1 > new_rating > 5):
            raise ValueError("Rating must be between 1 and 5")
        self._user_rating = new_rating

    def __repr__(self):
        if (self.podcast and self.episode):
            return f"Review {self.id}:\nPodcast: '{self.podcast.title}' | Episode: '{self.episode.title}'\nReviewer: {self.user}:\nRating: {self.user_rating}\nReview: {self.content}"
        elif self.podcast:
            return f"Review {self.id}:\nPodcast: '{self.podcast.title}'\nReviewer: {self.user}:\nRating: {self.user_rating}\nReview: {self.content}"
        else:
            return f"Review {self.id}:\nEpisode: '{self.episode.title}'\nReviewer: {self.user}:\nRating: {self.user_rating}\nReview: {self.content}"

    def __lt__(self, other):
        if not isinstance(other, Review):
            return False
        return self._id < other._id

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return self._id == other._id

    def __hash__(self):
        return hash((self.id, self.user_rating, self.content))


class Playlist:
    def __init__(self, playlist_id: int, playlist_owner: User, playlist_name: str = "Untitled"):
        validate_non_negative_int(playlist_id)
        self._id = playlist_id
        if not isinstance(playlist_owner, User):
            raise TypeError("playlist owner must be a User object")
        self._owner = playlist_owner
        validate_non_empty_string(playlist_name, "playlist title")
        self._title = playlist_name.strip()
        self._episodes = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "New title")
        self._title = new_title.strip()

    @property
    def episodes(self) -> list:
        return self._episodes

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Only episodes can be added to playlists")
        if episode not in self.episodes:
            self._episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self._episodes:
            self._episodes.remove(episode)

    def get_total_runtime(self) -> int:
        total_length = 0
        for episode in self._episodes:
            total_length += episode.length
        return total_length

    def __repr__(self):
        return f"<playlist {self.id}: '{self.title}' by user '{self.owner}' of length {len(self.episodes)}>"

    def __len__(self):
        return len(self._episodes)

    def __lt__(self, other):
        # episodes
        if not isinstance(other, Playlist):
            return False
        return len(self) < len(other)

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.id == other.id and self.owner.id == other.owner.id

    def __hash__(self):
        return hash((self.id, self.owner, self.title))

    def swap_element(self, i1: int, i2: int):
        self.episodes[i1], self.episodes[i2] = self.episodes[i2], self.episodes[i1]

    def shuffle(self) -> list:
        """Creates a new list object of shuffled episodes from this playlist"""
        shuffled_list = self.episodes.copy()
        random.shuffle(shuffled_list)
        return shuffled_list


class ModelException(Exception):
    pass


def make_review(review_id: int, content: str, user: User, podcast: Podcast,
                episode: Episode, rating: int, timestamp: datetime = datetime.now()):
    review = Review(review_id, user, rating, content, podcast, episode, timestamp)
    user.add_review(review)
    episode.add_review(review)

    return review


def make_category_association(podcast: Podcast, category: Category):
    if category.is_applied_to(podcast):
        raise ModelException(f'Category {category.name} already applied to Podcast "{podcast.title}"')

    podcast.add_category(category)
    category.add_podcast(podcast)
