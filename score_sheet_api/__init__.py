from flask import Flask
from flask_cors import CORS

app = Flask('score_sheet_api',static_url_path='/static')


app.debug = True
cors = CORS(app, resources={r"/*": {"origins": "*"}})
from score_sheet_api.src.controllers import *