from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

import podcast.adapters.repository as repo
import podcast.utilities.utilities as utilities
import podcast.episodes.services as services
import podcast.podcasts.services as podcast_services

from podcast.authentication.authentication import login_required

# Configure Blueprint.
episodes_blueprint = Blueprint(
    'episodes_bp', __name__)


@episodes_blueprint.route('/podcasts/<int:podcast_id>/episode/<int:episode_id>', methods=['GET'])
@login_required
def episode_detail(podcast_id, episode_id):
    podcast = podcast_services.podcast_id(podcast_id, repo.repo_instance)
    episode = services.get_episode(episode_id, repo.repo_instance)
    reviews = services.get_reviews_for_episode(episode_id, repo.repo_instance)
    username = session['user_name']

    user_playlist = None

    if username:
        user_name = session['user_name']
        user = services.get_user(repo.repo_instance, user_name)
        if user is not None:
            user_playlist = user.playlists


    page = request.args.get('page', 1, type=int)
    reviews_per_page = 6
    start_index = (page - 1) * reviews_per_page
    end_index = start_index + reviews_per_page
    paginated_reviews = episode['reviews'][start_index:end_index]
    total_pages = (len(episode['reviews']) + reviews_per_page - 1) // reviews_per_page

    return render_template(
        'episode/episodeDescription.html',
        podcast=podcast,
        episode=episode,
        reviews=paginated_reviews,
        page=page,
        total_pages=total_pages,
        user_playlist=user_playlist,
        max=max,
        min=min
    )


@episodes_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_on_episode():
    username = session['user_name']
    user = services.get_user(repo.repo_instance, username)
    if not user:
        # If no user is found in session, redirect to the login page
        return redirect(url_for('authentication_bp.login'))
    # Obtain username of the currently logged-in user
    user_name = session['user_name']

    # Create form. The form maintains state, e.g. when this method is called with an HTTP GET request and populates
    # the form with an episode id, when subsequently called with an HTTP POST request, the episode id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed validation.
        # Extract the episode id, representing the reviewed episode, from the form.
        episode_id = int(form.episode_id.data)
        podcast_id = int(form.podcast_id.data)

        # Use the service layer to store the new review
        services.add_review(podcast_id, episode_id, form.review.data, user_name, form.rating.data, repo.repo_instance)

        # Retrieve the episode in dict form
        episode = services.get_episode(episode_id, repo.repo_instance)

        # Cause the web browser to display reviewed episode and display reviews, including new review
        return redirect(url_for('episodes_bp.episode_detail', podcast_id=podcast_id, episode_id=episode_id))

    if request.method == 'GET':
        # Extract episode id, representing the episode to review, from a query parameter of the GET request.
        podcast_id = int(request.args.get('podcast'))
        episode_id = int(request.args.get('episode'))

        # Store the episode id in the form.
        form.episode_id.data = episode_id
        form.podcast_id.data = podcast_id

    else:
        # Extract the episode id of the episode being reviewed from the form.
        episode_id = int(form.episode_id.data)
        podcast_id = int(form.podcast_id.data)

    # For a GET or unsuccessful POST, retrieve the episode to review in dict form, and return
    # a web page that allows the user to enter a review. The generated web page includes a form object.
    episode = services.get_episode(episode_id, repo.repo_instance)
    podcast = podcast_services.podcast_id(podcast_id, repo.repo_instance)
    return render_template(
        'episode/review_on_episode.html',
        title='Edit episode',
        episode=episode,
        podcast=podcast,
        form=form,
        handler_url=url_for('episodes_bp.review_on_episode'),
    )


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short')])
    rating = IntegerField('Rating', [
        DataRequired(message="Rating is required"),
        NumberRange(min=1, max=5)
    ])
    episode_id = HiddenField("Episode id")
    podcast_id = HiddenField("Podcast id")
    submit = SubmitField('Submit')
