from abc import ABC
from typing import List

from sqlalchemy import desc, asc, func, delete, text
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from podcast.adapters.orm import playlists_episodes_association_table
from podcast.domainmodel.model import Author, User, Podcast, Episode, Review, Playlist, Category, PodcastSubscription
from podcast.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_author(self, author: Author):
        with self._session_cm as scm:
            scm.session.merge(author)
            scm.commit()

    def get_author(self, author_name: str) -> Author:
        author = None
        try:
            author = self._session_cm.session.query(Author).filter(Author._name == author_name).one()
        except NoResultFound:
            pass

        return author

    def add_podcast(self, podcast: Podcast):
        with self._session_cm as scm:
            scm.session.merge(podcast)
            scm.commit()

    def get_podcast(self, podcast_id) -> Podcast:
        podcast = None
        try:
            podcast = self._session_cm.session.query(Podcast).filter(Podcast._id == podcast_id).one()
        except NoResultFound:
            pass

        return podcast

    def get_number_of_podcasts(self) -> int:
        number_of_podcasts = self._session_cm.session.query(Podcast).count()
        return number_of_podcasts

    def get_podcasts_by_id(self, id_list):
        podcasts = self._session_cm.session.query(Podcast).filter(Podcast._id.in_(id_list)).all()
        return podcasts

    def get_list_of_podcasts(self):
        return self._session_cm.session.query(Podcast).order_by(asc(Podcast._title)).all()

    def get_podcast_ids_by_category(self, category_name: str):
        podcast_ids = []

        # Use text() to declare SQL queries
        row = self._session_cm.session.execute(
            text('SELECT id FROM categories WHERE name = :category_name'),
            {'category_name': category_name}
        ).fetchone()

        if row is not None:
            category_id = row[0]
            podcast_ids = self._session_cm.session.execute(
                text(
                    'SELECT podcast_id FROM podcasts_categories WHERE category_id = :category_id ORDER BY podcast_id ASC'),
                {'category_id': category_id}
            ).fetchall()
            podcast_ids = [id[0] for id in podcast_ids]

        return podcast_ids

    def get_podcast_ids_by_language(self, language: str):
        # Actually returns podcasts, but I don't think this method gets used anyway.
        podcasts = self._session_cm.session.query(Podcast).filter(Podcast._language == language).all()
        return podcasts

    def add_category(self, category: Category):
        with self._session_cm as scm:
            scm.session.merge(category)
            scm.commit()

    def get_categories(self):
        categories = self._session_cm.session.query(Category).all()
        return categories

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def get_user(self, user_name: str):
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._username == user_name.lower()).one()
        except NoResultFound:
            pass

        return user

    def get_number_of_users(self) -> int:
        number_of_users = self._session_cm.session.query(User).count()
        return number_of_users

    def add_podcast_subscription(self, subscription: PodcastSubscription):
        # Unimplemented
        return None

    def get_podcast_subscription(self, sub_id) -> PodcastSubscription:
        # Unimplemented
        return None

    def add_episode(self, episode: Episode):
        with self._session_cm as scm:
            scm.session.merge(episode)
            scm.commit()

    def get_episode(self, episode_id):
        episode = None
        try:
            episode = self._session_cm.session.query(Episode).filter(Episode._id == episode_id).one()
        except NoResultFound:
            pass

        return episode

    def get_number_of_episodes(self) -> int:
        number_of_episodes = self._session_cm.session.query(Episode).count()
        return number_of_episodes

    def get_first_episode(self):
        episode = self._session_cm.session.query(Episode).first()
        return episode

    def get_last_episode(self):
        episode = self._session_cm.session.query(Episode).order_by(desc(Episode._id)).first()
        return episode

    def get_episodes_by_id(self, id_list):
        episodes = self._session_cm.session.query(Episode).filter(Episode._id.in_(id_list)).all()
        return episodes

    def get_next_episode_id(self, episode: Episode):
        # Unimplemented
        return None

    def get_previous_episode_id(self, episode: Episode):
        # Unimplemented
        return None

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.merge(review)
            scm.commit()

    def get_reviews(self):
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def get_number_of_reviews(self) -> int:
        number_of_reviews = self._session_cm.session.query(Review).count()
        return number_of_reviews

    def add_playlist(self, playlist: Playlist):
        with self._session_cm as scm:
            scm.session.add(playlist)
            scm.commit()

    def get_playlists(self):
        playlists = self._session_cm.session.query(Playlist).all()
        return playlists

    def add_episode_to_playlist(self, user: User, episode: Episode):
        with self._session_cm as scm:
            playlist = user.playlists[0]
            playlist.add_episode(episode)
            scm.session.merge(episode)
            scm.session.merge(playlist)
            scm.commit()

    def remove_episode_from_playlist(self, user: User, episode: Episode):
        with self._session_cm as scm:
            # Set busy timeout to avoid "database is locked" errors

            # Query the user's playlist
            playlist = scm.session.query(Playlist).filter(Playlist._owner == user).one_or_none()

            if not playlist:
                raise ValueError(f"Playlist for user {user.id} not found.")

            # Ensure the episode is in the playlist
            if episode not in playlist.episodes:
                raise ValueError(f"Episode {episode.id} not found in user's playlist.")

            # Remove the episode from the playlist
            playlist.remove_episode(episode)

            # Delete the episode from the database
            scm.session.delete(episode)
            scm.commit()



