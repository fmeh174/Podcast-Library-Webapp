from flask import Blueprint, request, render_template, redirect, url_for, session, flash, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length

import podcast.adapters.repository as repo
import podcast.playlist.services as services
from podcast.authentication.authentication import login_required
from podcast.podcasts.services import podcast_id

# Configure Blueprint for Playlists
playlists_blueprint = Blueprint(
    'playlists_bp', __name__
)



@playlists_blueprint.route('/add_episode', methods=['GET', 'POST'])
@login_required
def add_episode_to_playlist():
    username = session['user_name']
    if not username:
        return redirect(url_for('authentication_bp.login'))

    episode_id = request.args.get('episode_id')

    username = session['user_name']
    user = services.get_user(repo.repo_instance, username)

    episode = services.get_episode(repo.repo_instance, episode_id)  # Fetch the episode object by id

    if user:
        if current_app.config['REPOSITORY'] == 'database':
            repo.repo_instance.add_episode_to_playlist(user, episode)
        else:
            user.add_episode_to_playlist(episode)
    flash('Episode successfully added.', 'success')
    return redirect(url_for('playlists_bp.view_playlists'))


@playlists_blueprint.route('/remove_episode', methods=['POST', 'GET'])
@login_required
def remove_episode_from_playlist():
    username = session.get('user_name')
    if not username:
        flash('You need to be logged in to remove an episode from your playlist.', 'error')
        return redirect(url_for('authentication_bp.login'))

    episode_id = request.args.get('episode_id')

    user = services.get_user(repo.repo_instance, username)

    episode = services.get_episode(repo.repo_instance, episode_id)

    if episode is None:
        flash(f'Episode with ID {episode_id} not found.', 'error')
        return redirect(url_for('playlists_bp.view_playlists'))
    if current_app.config['REPOSITORY'] == 'database':
        repo.repo_instance.remove_episode_from_playlist(user, episode)
    else:
        user.remove_episode_from_playlist(episode)
    flash('Episode successfully removed.', 'success')
    return redirect(url_for('playlists_bp.view_playlists'))

@playlists_blueprint.route('/view', methods=['GET'])
@login_required
def view_playlists():
    user_name = session['user_name']
    if not user_name:
        return redirect(url_for('authentication_bp.register'))

    user = services.get_user(repo.repo_instance, user_name)

    if user is None:
        return redirect(url_for('authentication_bp.register'))

    if current_app.config['REPOSITORY'] == 'database':
        playlist = user.playlists[0] if user.playlists else None
        if playlist is None:
            return "No playlists found."
        podcasts = {}

        for episode in playlist.episodes:
            episode_podcast_id = episode.podcast.id
            podcast = services.get_podcast(repo.repo_instance, episode_podcast_id)

            if podcast in podcasts:
                podcasts[podcast].append(episode)
            else:
                podcasts[podcast] = [episode]

    else:
        playlists = user.playlists
        podcasts = {}
        for episode in playlists:
            episode_podcast_id = episode.podcast.id
            podcast = services.get_podcast(repo.repo_instance, episode_podcast_id)

            # If the podcast is already in the dictionary, append the episode to its list
            if podcast in podcasts:
                podcasts[podcast].append(episode)
            else:
                # If the podcast is not in the dictionary, add it with the episode in a new list
                podcasts[podcast] = [episode]

    return render_template(
        'playlist/view_playlists.html',
        username=user_name,
        podcasts=podcasts

    )

@playlists_blueprint.route('/add_podcast', methods=['GET', 'POST'])
@login_required
def add_podcast_to_playlist():
    username = session.get('user_name')
    if not username:
        # If no user is found in session, redirect to the login page
        return redirect(url_for('authentication_bp.login'))

    new_podcast_id = request.args.get('podcast_id')
    user = services.get_user(repo.repo_instance, username)

    # Fetch the podcast object by id
    podcast = services.get_podcast(repo.repo_instance, new_podcast_id)

    if user and podcast:
        for episodes in podcast.episodes:
            if current_app.config['REPOSITORY'] == 'database':
                repo.repo_instance.add_episode_to_playlist(user, episodes)
            else:
                user.add_episode_to_playlist(episodes)
        flash('Podcast successfully added to the playlist.', 'success')
    else:
        flash('Podcast or user not found.', 'error')

    return redirect(url_for('playlists_bp.view_playlists'))
