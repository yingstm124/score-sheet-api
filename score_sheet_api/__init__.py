from flask import Flask
from flask_cors import CORS

app = Flask('ScoreSheet_api',static_url_path='/static')


app.debug = True
cors = CORS(app, resources={r"/*": {"origins": "*"}})
from ScoreSheet_api.controllers import *