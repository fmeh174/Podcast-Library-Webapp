from pathlib import Path

from podcast.adapters.repository import AbstractRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.domainmodel.model import Author


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool = False):
    data_reader = CSVDataReader(data_path / "podcasts.csv", data_path / "episodes.csv")
    data_reader.load_podcasts(database_mode)
    data_reader.load_episodes()

    for podcast in data_reader.podcasts.values():
        repo.add_podcast(podcast)

    for episode in data_reader.episodes:
        repo.add_episode(episode)

    for author_name in data_reader.authors.keys():
        author = Author(data_reader.authors[author_name], author_name)
        repo.add_author(author)

    for category in data_reader.categories.values():
        repo.add_category(category)
