import csv
from datetime import datetime
from podcast.domainmodel.model import Podcast, Episode, Author, Category, make_category_association
from typing import List

from path_utils.utils import get_project_root


class CSVDataReader:
    # TODO: Complete the implementation of the CSVDataReader class.
    def __init__(self, podcasts_file=get_project_root() / "podcast" / "adapters" / "data" / "podcasts.csv",
                 episodes_file=get_project_root() / "podcast" / "adapters" / "data" / "episodes.csv"):
        self.__podcasts_filename = str(podcasts_file)
        self.__episodes_filename = str(episodes_file)
        self.podcasts = dict()
        self.episodes: List[Episode] = []
        self.authors = dict()   # Name: ID. Provides easy access for CSVDataReader methods.
        self.categories = dict()

    def load_episodes(self):
        """Loads episodes from csv file into self.episodes.
        Code borrowed and refactored from both Faiza and Gurrnor."""
        for data_row in read_csv_file(self.__episodes_filename):
            podcast = self.podcasts.get(int(data_row[1]))
            episode = Episode(
                episode_id=int(data_row[0]),
                podcast=podcast,
                episode_title=data_row[2],
                episode_audio=data_row[3],
                episode_length=int(data_row[4]),
                episode_desc=data_row[5],
                upload_date=to_strptime(data_row[6]),
            )
            self.episodes.append(episode)

    def load_authors(self):
        """Reads the podcasts.csv file to load all author and category objects."""
        # Only creates objects if it's the first time.
        if len(self.authors) == 0:
            self.create_authors()

    def create_authors(self):
        """Reads the podcasts.csv file to create all the author objects."""

        # I'm putting this here pre-emptively to handle cases where a podcast is missing an Author.
        # TODO: Set this Author as the default Author object when Author missing from Podcast.
        blank_author = missing_author()
        self.authors[blank_author.name] = blank_author.id

        author_id = 2  # ID of 1 is reserved for "missing" authors.
        for data_row in read_csv_file(self.__podcasts_filename):

            author_name = data_row[7].strip()
            # Checks if author exists. If so, proceed as normal. Else, no author is added.
            if len(author_name) > 0:
                # Checking if the author is in the dict
                if author_name not in self.authors:
                    self.authors[author_name] = author_id
                    author_id += 1

    def load_podcasts(self, database_mode: bool = False):
        categories_and_podcasts = dict()

        self.load_authors()

        for data_row in read_csv_file(self.__podcasts_filename):

            podcast_key = int(data_row[0])
            podcast_categories = [category_name.strip() for category_name in data_row[5].split("|")]

            # Add new categories; associate the current Podcast with categories.
            for category in podcast_categories:
                if category not in categories_and_podcasts.keys():
                    categories_and_podcasts[category] = list()
                categories_and_podcasts[category].append(podcast_key)

            # Create Author object.
            if data_row[7] == "" or data_row[7] is None:
                author = missing_author()
            else:
                author = Author(self.authors[data_row[7]], data_row[7])

            # Create Podcast object.
            podcast = Podcast(
                podcast_id=int(data_row[0]),
                author=author,
                title=data_row[1],
                image=data_row[2],
                description=data_row[3],
                website=data_row[6],
                itunes_id=int(data_row[8]),
                language=data_row[4],
            )
            self.podcasts[podcast.id] = podcast

        category_id = 1

        # Create category objects, associate them with Podcasts.
        for category_name in categories_and_podcasts.keys():
            category = Category(category_id, category_name)
            for podcast_id in categories_and_podcasts[category_name]:
                podcast = self.podcasts[podcast_id]
                if database_mode is True:
                    # The ORM takes care of the association between podcasts and categories
                    podcast.add_category(category)
                else:
                    make_category_association(podcast, category)
            self.categories[category_id] = category
            category_id += 1


def read_csv_file(filename: str):
    """Helper function by Faiza to read the csv file for CSVDataReader methods."""
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        for row in reader:
            row = [item.strip() for item in row]
            yield row


def to_strptime(date_string: str):
    """Converts the string format of datetime from episodes.csv into strptime datetime object."""
    date_format = "%Y-%m-%d %H:%M:%S%z"
    date_strp = date_string
    date_strp += "00"  # Makes +UTC valid format without adding information
    return datetime.strptime(date_strp, date_format)


def missing_author():
    return Author(1, "MISSING: No Author provided")


def missing_category():
    return Category(1, "MISSING CATEGORY")
