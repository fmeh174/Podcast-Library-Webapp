import pytest

from flask import session
from podcast.authentication import services as auth_services


def test_register(client):
    # Check that we receive the register page
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a User successfully, supplying a valid user and pass
    response = client.post(
        '/authentication/register',
        data={'user_name': 'Mario', 'password': 'ILoveMushrooms123'}
    )
    assert response.headers['Location'] == "/authentication/login"


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Username required'),
        ('m', '', b'Username has a minimum length of 3'),
        ('test', '', b'Input password'),
        ('test', 'test', b'Your password must be at least 8 characters, contain one number, one uppercase letter,\
             and one lowercase letter'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    response = client.post(
        'authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    test_register(client)
    # Check that we recieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login redirects to home
    response = auth.login()
    assert response.headers['Location'] == '/'

    # Check that a session has been created
    with client:
        client.get('/')
        assert session['user_name'] == 'mario'


def test_logout(client, auth):
    test_login(client, auth)

    with client:
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Fetch home
    response = client.get("/")
    assert response.status_code == 200
    assert b"CS235 Podcast Library" in response.data


def test_login_required_to_review(client):
    response = client.post("/review?podcast=14&episode=1")
    assert response.headers['Location'] == "/authentication/login"


def test_review(client, auth):
    test_login(client, auth)

    response = client.get('/review?podcast=14&episode=1')

    response = client.post(
        '/review?podcast=14&episode=1',
        data={'review': 'Great episode!', 'rating': 5, 'episode_id': 1, 'podcast_id': 14}
    )
    assert response.headers['Location'] == '/podcasts/14/episode/1'


def test_review_with_invalid_input(client, auth):
    test_login(client, auth)

    response = client.post(
        '/review?podcast=14&episode=1',
        data={'review': "T", 'rating': 5, 'episode_id': 1, 'podcast_id': 14}
    )

    assert b'Your review is too short' in response.data


def test_podcast_browsing(client):
    response = client.get("/podcasts")
    assert response.status_code == 200

    assert b'D-Hour Radio Network' in response.data
    assert b'Brian Denny Radio' in response.data
