from flask_mail import Message
from ksk import mail,app
from flask import url_for
import secrets
import os
from PIL import Image


def send_mail(user):
    token = user.generate_token()
    msg = Message('Password Reset Request',sender='noreply@demo.com',recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{ url_for('users.reset_token',token=token,_external=True) }    

If you did not make this request then simply ignore this email and no changes will be made
    '''
    mail.send(msg)

def save_img_for_pizza(image):
    hex_code = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(image.filename)
    picture_filename = hex_code + f_ext
    picture_filepath = os.path.join(app.root_path,'static/product_images/pizza',picture_filename)

    output_size = (300,128)
    i = Image.open(image)
    i.thumbnail(output_size)

    i.save(picture_filepath)
    return picture_filename

def save_img_for_breadsnack(image):
    hex_code = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(image.filename)
    picture_filename = hex_code + f_ext
    picture_filepath = os.path.join(app.root_path,'static/product_images/breadsnack',picture_filename)

    output_size = (300,128)
    i = Image.open(image)
    i.thumbnail(output_size)

    i.save(picture_filepath)
    return picture_filename