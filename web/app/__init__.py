import os
import json
import datetime
from flask import Flask
from app.controller import main_interface
from app.controller import mongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'bilibili'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/bilibili'
mongo.__init__(app)
app.register_blueprint(main_interface)

