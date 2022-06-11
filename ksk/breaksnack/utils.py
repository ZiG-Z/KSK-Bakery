import os
import secrets
from PIL import Image
from ksk import app

def save_img_for_breadsnack(image):
    hex_code = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(image.filename)
    picture_filename = hex_code + f_ext
    save_pic_in_filepath = os.path.join(app.root_path,'static/product_images/breadsnack',picture_filename)

    output_size = (300,128)
    i = Image.open(image)
    i.thumbnail(output_size)

    i.save(save_pic_in_filepath)
    return picture_filename
