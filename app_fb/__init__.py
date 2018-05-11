from flask import Flask
from flask_cors import CORS

app = Flask('app_fb',
            static_folder='./static',
            static_url_path='',
            template_folder='./templates')
CORS(app)

from app_fb import views, api
