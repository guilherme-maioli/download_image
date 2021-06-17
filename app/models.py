
from app import db

class Words(db.Model):
	__tablename__ = "words"
	id = db.Column(db.Integer, primary_key=True)
	word_from = db.Column(db.String(100), nullable=False)
	word_to = db.Column(db.String(100))

