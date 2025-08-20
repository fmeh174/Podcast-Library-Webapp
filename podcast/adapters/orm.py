from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime, ForeignKey)
from sqlalchemy.orm import registry, relationship, synonym

from podcast.domainmodel import model

# global variable giving access to the MetaData (schema) information of the database
mapper_registry = registry()

authors_table = Table(
    'authors', mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), unique=True, nullable=False)
)

podcasts_table = Table(
    'podcasts', mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('author_id', ForeignKey('authors.id')),
    Column('title', String(255), nullable=True),
    Column('image_url', String(255), nullable=True),
    Column('description', String(255), nullable=True),
    Column('language', String(255), nullable=True),
    Column('website_url', String(255), nullable=True),
    Column('itunes_id', Integer, nullable=True)
)

episodes_table = Table(
    'episodes', mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('podcast_id', ForeignKey('podcasts.id')),
    Column('title', String(255), nullable=True),
    Column('audio_url', String(255), nullable=True),
    Column('description', String(255), nullable=True),
    Column('upload_date', DateTime, nullable=True)
    # I'm excluding episode length.
)

categories_table = Table(
    'categories', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

podcasts_categories_association_table = Table(
    'podcasts_categories', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.id')),
    Column('category_id', ForeignKey('categories.id'))
)

users_table = Table(
    'users', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(64), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('podcast_id', ForeignKey('podcasts.id')),
    Column('episode_id', ForeignKey('episodes.id')),
    Column('rating', Integer, nullable=False),
    Column('content', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

playlists_table = Table(
    'playlists', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('owner_id', ForeignKey('users.id')),
    Column('title', String(255), nullable=False)
)

playlists_episodes_association_table = Table(
    'playlists_episodes', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('playlist_id', ForeignKey('playlists.id')),
    Column('episode_id', ForeignKey('episodes.id'))
)


def map_model_to_tables():
    mapper_registry.map_imperatively(model.Author, authors_table, properties={
        '_id': authors_table.c.id,
        '_name': authors_table.c.name,
    })

    mapper_registry.map_imperatively(model.Podcast, podcasts_table, properties={
        '_id': podcasts_table.c.id,
        '_author': relationship(model.Author),
        '_title': podcasts_table.c.title,
        '_image': podcasts_table.c.image_url,
        '_description': podcasts_table.c.description,
        '_language': podcasts_table.c.language,
        '_website': podcasts_table.c.website_url,
        '_itunes_id': podcasts_table.c.itunes_id,
        'episodes': relationship(model.Episode, back_populates='_podcast'),
        'categories': relationship(model.Category, secondary=podcasts_categories_association_table),
    })

    mapper_registry.map_imperatively(model.Episode, episodes_table, properties={
        '_id': episodes_table.c.id,
        '_podcast': relationship(model.Podcast, back_populates='episodes'),
        '_title': episodes_table.c.title,
        '_audio': episodes_table.c.audio_url,
        '_description': episodes_table.c.description,
        '_upload_date': episodes_table.c.upload_date,
        '_reviews': relationship(model.Review, back_populates='_episode')
    })

    mapper_registry.map_imperatively(model.Category, categories_table, properties={
        '_id': categories_table.c.id,
        '_name': categories_table.c.name
    })

    mapper_registry.map_imperatively(model.User, users_table, properties={
        '_id': users_table.c.id,
        '_username': users_table.c.user_name,
        '_password': users_table.c.password,
        '_reviews': relationship(model.Review, back_populates='_user'),
        '_playlists': relationship(model.Playlist, back_populates='_owner')
    })

    mapper_registry.map_imperatively(model.Review, reviews_table, properties={
        '_id': reviews_table.c.id,
        '_podcast': relationship(model.Podcast),
        '_episode': relationship(model.Episode, back_populates='_reviews'),
        '_user': relationship(model.User, back_populates='_reviews'),
        '_user_rating': reviews_table.c.rating,
        '_content': reviews_table.c.content,
        '_post_date': reviews_table.c.timestamp
    })

    mapper_registry.map_imperatively(model.Playlist, playlists_table, properties={
        '_id': playlists_table.c.id,
        '_owner': relationship(model.User, back_populates='_playlists'),
        '_title': playlists_table.c.title,
        '_episodes': relationship(model.Episode, secondary=playlists_episodes_association_table)
    })
