from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SECRET_KEY"] = "4654f5dfadsrfasdr54e6rae"
fastapi_url = "http://fastapi-backend:1337"

bcrypt = Bcrypt(app)

import frontend.routes
