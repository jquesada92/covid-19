from layout import layout
from callbacks import register_Callback
from flask import Flask
from flask_caching import Cache
import dash
from datetime import datetime, timedelta


def create_app():
        server = Flask(__name__)
        app = dash.Dash(__name__,server=server)
        app.config.suppress_callback_exceptions = True
        index_string = open('./templates/index.html', 'r').read()
        app.index_string = index_string
        app.layout = layout
        register_Callback(app)
        return server,app