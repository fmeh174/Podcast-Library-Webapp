import random
from flask import Blueprint, render_template


import podcast.utilities.utilities as utilities
import podcast.adapters.repository as repo
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    podcast_count = repo.repo_instance.get_number_of_podcasts()
    return render_template(
        'home/home.html',
    )

# TODO: Implement home() blueprint
