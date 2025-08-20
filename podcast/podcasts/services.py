from typing import List, Iterable

from sqlalchemy.orm.collections import InstrumentedList

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Category, Episode
from podcast.episodes.services import episode_to_dict, episodes_to_dict


def get_number_of_podcasts(repo: AbstractRepository):
    return repo.get_number_of_podcasts()


def podcast_id(id: int, repo: AbstractRepository):
    podcasts = get_podcast_dicts(repo)
    return podcasts[id]


class PodcastDicts:
    podcast_dicts = {}


def get_podcast_dicts(repo: AbstractRepository):
    podcasts = repo.get_list_of_podcasts()
    if PodcastDicts.podcast_dicts == {} or repo.get_number_of_podcasts() < 50:
        for podcast in podcasts:
            podcast_dict = podcast_to_dict(podcast)
            PodcastDicts.podcast_dicts[podcast_dict["id"]] = podcast_dict
    return PodcastDicts.podcast_dicts


def search_podcast(query: str, filter_by: str, repo: AbstractRepository) -> List[dict]:
    podcasts = repo.get_list_of_podcasts()
    query_lower = query.lower()  #lowercase
    matching_podcasts = []

    for podcast in podcasts:
        if filter_by == 'title' and query_lower in podcast.title.lower():
            matching_podcasts.append(podcast_to_dict(podcast))
        elif filter_by == 'category':
            for category in podcast.categories:
                if query_lower in category.name.lower():
                    matching_podcasts.append(podcast_to_dict(podcast))
                    break
        elif filter_by == 'author' and query_lower in podcast.author.name.lower():
            matching_podcasts.append(podcast_to_dict(podcast))

    return matching_podcasts


def podcast_to_dict(podcast: Podcast):
    podcast_dict = {
        'id': podcast.id,
        'author': podcast.author,
        'title': podcast.title,
        'image': podcast.image,
        'description': podcast.description,
        'website': podcast.website,
        'itunes_id': podcast.itunes_id,
        'language': podcast.language,
        'categories': categories_to_string(podcast.categories),     # Categories current unimplemented.
        'episodes': episodes_to_dict(podcast.episodes)
    }
    return podcast_dict


def category_to_dict(category: Category):
    category_dict = {
        'id': category.id,
        'name': category.name,
    }
    return category_dict


def categories_to_dict(categories: Iterable[Category]):
    return [category_to_dict(category) for category in categories]


def categories_to_string(categories: Iterable[Category]):
    categories_list = categories_to_dict(categories)
    categories_string = " | ".join([category['name'] for category in categories_list])
    return categories_string
