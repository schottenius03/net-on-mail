from flask import Flask 		# importera "Flask" från paketet "flask"
from my_server.config import Config

app = Flask(__name__)			# skapa variabeln "app"
app.config.from_object(Config)

from my_server import routes, error	# importera (och kör) modulen "routes & errors"