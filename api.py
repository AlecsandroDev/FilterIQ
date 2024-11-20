from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv

app = Flask(__name__)
CORS(app)

from routes import *

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, port=getenv("port"))