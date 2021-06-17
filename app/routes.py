from app.download import download as download_blueprint
from app.words import words as words_blueprint

def init_app(app):
	app.register_blueprint(download_blueprint)
	app.register_blueprint(words_blueprint)