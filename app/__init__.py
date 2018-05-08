from flask import Flask

app = Flask('mini_amazon',
            static_folder='./static',
            static_url_path='',
            template_folder='./templates')

from mini_amazon import views, api