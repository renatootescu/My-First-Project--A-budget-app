import os  # the os module allows for the user image to be saved on the hdd
import secrets  # module that generates unique tokens
from PIL import Image  # module that allows for image manipulation
from flask import url_for, current_app  # flask modules
from flask_mail import Message  # module used to generate the reset password mail
from budget import mail  # used to send the reset password mail


def save_picture(form_picture):
    """Adding and resizing the account image"""
    random_hex = secrets.token_hex(8)  # generate unique token for the image
    _, f_ext = os.path.splitext(form_picture.filename)  # loading image from form
    picture_fn = random_hex + f_ext  # generate image key
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)  # generate the save path for the image

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    """generate and send the reset password mail"""
    token = user.get_reset_token()  # new unique token
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request please ignore this email. No changes will be made.
'''
    mail.send(msg)
