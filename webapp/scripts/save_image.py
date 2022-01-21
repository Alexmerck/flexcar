from flask import request
from flask_login.utils import login_required
from flask import  abort
from config import Config
import imghdr, secrets
import os


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


def upload_files():
    if request.files['file']:
        uploaded_file = request.files['file']
        file_name = uploaded_file.filename
        file_ext = os.path.splitext(file_name)[1].lower()
        image_name = f"{secrets.token_hex(8)}{file_ext}"
        if file_ext not in Config.UPLOAD_EXTENSIONS or \
            file_ext != validate_image(uploaded_file.stream):
            raise ValueError
        uploaded_file.save(os.path.join(Config.UPLOAD_PATH, image_name))
    else:
        image_name = "default.jpg"
    return image_name
