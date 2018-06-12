# Generating custom error pages

from flask import Blueprint, render_template  # Blueprint allows us to create application components

errors = Blueprint('errors', __name__)  # instantiate the errors Blueprint


# creating the errors routes
@errors.app_errorhandler(404)  # the errors decorator allows Flask to pass error messages to the frontend
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
