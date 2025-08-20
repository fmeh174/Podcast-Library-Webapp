from flask import Blueprint, request, render_template, redirect, url_for, session

import podcast.adapters.repository as repo
import podcast.utilities.services as services

# Configure blueprint
utilities_blueprint = Blueprint('utilities_bp', __name__)


def get_selected_podcast(quantity=3):
    podcasts = (services.get_random_podcasts(quantity, repo.repo_instance))
    for podcast in podcasts:
        podcast['hyperlink'] = url_for('podcast_bp.podcast_detail', id=podcast['id'])
    return podcasts


def get_categories_and_urls():
    category_names = services.get_category_names(repo.repo_instance)
    category_urls = dict()
    for category_name in category_names:
        category_urls[category_name] = url_for('podcast_bp.podcasts_by_category', category=category_name)
    return category_urls
