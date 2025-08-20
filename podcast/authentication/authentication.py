from flask import Blueprint, render_template, redirect, url_for, session, flash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps

# Maybe import Utils, we'll see
import podcast.authentication.services as services
import podcast.adapters.repository as repo

# Config Blueprint
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None

    if form.validate_on_submit():
        # Successful POST request if username and password pass validation checking
        # Service layer attempts to add the new user.
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            flash('Registration successful! Please log in.', 'success')

            # Redirect user to login page
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            user_name_not_unique = 'Username already taken. Please try another'
            flash(user_name_not_unique, 'error')

    # During a GET or a failed POST request, return registration page
    return render_template(
        'authentication/credentials.html',
        title='Register',
        form=form,
        user_name_error_message=user_name_not_unique,
        handler_url=url_for('authentication_bp.register'),
        button_text='Register'
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name_not_recognised = None
    incorrect_password_provided = None

    if form.validate_on_submit():
        # Successful POST request if username and password pass validation checking
        # Service layer does a lookup on the user
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)

            # Auth user
            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)

            # Init new session and redirect to homepage =D
            session.clear()
            session['user_name'] = user['user_name']
            flash(f'Welcome, {user["user_name"]}! You have been logged in.', 'success')
            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            # Username not known to the system
            user_name_not_recognised = 'No account found please register'
            flash(user_name_not_recognised, 'error')

        except services.AuthenticationException:
            # Authentication failed
            incorrect_password_provided = 'Incorrect password. Try again'
            flash(incorrect_password_provided, 'error')

    # During a GET or a failed POST request, return registration page
    return render_template(
        'authentication/credentials.html',
        title='Login',
        user_name_error_message=user_name_not_recognised,
        password_error_message=incorrect_password_provided,
        form=form,
        handler_url=url_for('authentication_bp.login'),
        button_text = 'Login',
    )


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home_bp.home'))



def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            flash('You need to log in to access this page.', 'error')
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, contain one number, one uppercase letter,\
             and one lowercase letter'
            self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema.min(8) \
                .has().digits() \
                .has().uppercase() \
                .has().lowercase()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField('Username:', [
        DataRequired(message='Username required'),
        Length(min=3, message='Username has a minimum length of 3')])
    password = PasswordField('Password:', [
        DataRequired(message='Input password'),
        PasswordValid()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    user_name = StringField('Username:', [
        DataRequired()])
    password = PasswordField('Password:', [
        DataRequired()])
    submit = SubmitField('Submit')
