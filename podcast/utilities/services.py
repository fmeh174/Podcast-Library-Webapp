from typing import Iterable
import random

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast


def get_category_names(repo: AbstractRepository):
    categories = repo.get_categories()
    category_names = [category.name for category in categories]

    return category_names


def get_random_podcasts(quantity, repo: AbstractRepository):
    podcast_count = repo.get_number_of_podcasts()

    if quantity >= podcast_count:
        # Reduce quantity if higher than the number of podcasts in repo
        quantity = quantity - 1

    random_ids = random.sample(range(1, podcast_count), quantity)
    podcasts = repo.get_podcasts_by_id(random_ids)

    return podcasts_to_dict(podcasts)

# Functions to convert to dicts

def podcast_to_dict(podcast: Podcast):
    podcast_dict = {
        'author': podcast.author,
        'title': podcast.title,
        'image_hyperlink': podcast.image,
        'language': podcast.language
    }
    return podcast_dict


def podcasts_to_dict(podcasts: Iterable[Podcast]):
    return [podcast_to_dict(podcast) for podcast in podcasts]