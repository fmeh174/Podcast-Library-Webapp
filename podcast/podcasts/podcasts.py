from datetime import date
import math
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

import podcast.podcasts.services as services
import podcast.adapters.repository as repo

podcasts_blueprint = Blueprint('podcasts_bp', __name__)


# TODO: Implement podcasts_bp

@podcasts_blueprint.route('/podcasts/<int:id>', methods=['GET'])
def podcast_detail(id):
    podcast = services.podcast_id(id, repo.repo_instance)
    page = request.args.get('page', 1, type=int)
    episodes_per_page = 6
    start_index = (page - 1) * episodes_per_page
    end_index = start_index + episodes_per_page
    paginated_episodes = podcast['episodes'][start_index:end_index]
    total_pages = (len(podcast['episodes']) + episodes_per_page - 1) // episodes_per_page
    return render_template(
        'podcastDescription.html',
        title=f'{podcast["title"]} | CS235 Pod Library',
        podcast=podcast,
        podcast_categories=podcast["categories"],
        episodes=paginated_episodes,
        page=page,
        total_pages=total_pages,
        max=max,
        min=min
    )


@podcasts_blueprint.route('/search', methods=['GET'])
def search_podcast():
    query = request.args.get('query', '')
    filter_by = request.args.get('filter', 'title')
    page = request.args.get('page', 1, type=int)
    per_page = 15
    search_results = services.search_podcast(query, filter_by, repo.repo_instance)
    total_results = len(search_results)
    total_pages = (total_results + per_page - 1) // per_page
    paginated_results = search_results[(page - 1) * per_page:page * per_page]

    return render_template(
        'podcasts.html',
        search_results=paginated_results,
        total_pages=total_pages,
        page=page,
        query=query,
        filter_by=filter_by,
        max=max,
        min=min
    )


@podcasts_blueprint.route('/podcasts', methods=['GET'])
def browse_podcast():
    page = request.args.get('page', 1, type=int)
    per_page = 15
    num_podcast = services.get_number_of_podcasts(repo.repo_instance)
    all_podcast = list(services.get_podcast_dicts(repo.repo_instance).values())
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_podcasts = all_podcast[start_index:end_index]

    return render_template(
        'podcasts.html',
        title=f'Browse page | CS235 Pod Library',
        heading='Browse Podcast',
        num_podcast=num_podcast,
        podcasts=paginated_podcasts,
        page=page,
        total_pages=math.ceil(num_podcast / per_page),
        max=max,
        min=min
    )
