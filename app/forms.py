from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField, SubmitField
from wtforms.validators import Length, DataRequired

class WordForm(FlaskForm):
	word_from = StringField("De:", validators=[
			DataRequired("O campo é obrigatório"),
			Length(1, 100, "O campo deve conter entre 1 a 100 caracteres")
		])
	word_to = StringField("Para:", validators=[
			Length(1, 100, "O campo deve conter entre 1 a 100 caracteres")
		])
	submit = SubmitField("Cadastrar")