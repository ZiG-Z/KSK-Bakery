import secrets
import os
from PIL import Image
from ksk import app

def save_img_for_pizza(image):
    hex_code = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(image.filename)
    pic_filename = hex_code + f_ext
    save_pic_in_filepath = os.path.join(app.root_path,'static/product_images/pizza',pic_filename)

    output_size = (300,128)
    i = Image.open(image)
    i.thumbnail(output_size)

    i.save(save_pic_in_filepath)
    return pic_filename