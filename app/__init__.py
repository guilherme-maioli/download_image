from flask import Flask 
import os
from flask_sqlalchemy import SQLAlchemy 
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()

def create_app():

	app = Flask(__name__)
	app.config["SECRET_KEY"] = "secret"
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


	APP_ROOT = os.path.dirname(os.path.abspath(__file__)) # pega o caminho download/app
	UPLOAD_FOLDER = os.path.dirname(APP_ROOT)
	UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, "images")
	
	#UPLOAD_FOLDER = APP_ROOT.replace("app", "./Donwload")
	
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

	db.init_app(app)
	bootstrap.init_app(app)

	from app import routes
	routes.init_app(app)

	return app