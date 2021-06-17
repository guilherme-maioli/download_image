from . import words

from app.forms import WordForm
from app import db
from app.models import Words
from app.words.description import validate_description

from flask import current_app
from flask import render_template, flash, redirect, url_for, request, send_file
from sqlalchemy import desc
from pandas import read_excel
import os



@words.route("/", methods=["GET", "POST"])
def index():
	return redirect(url_for("download.download_image"))

@words.route("/words", methods=["GET", "POST"])
def list_words():
	#words_list = Words.query.all()
	words_list = db.session.query(Words).order_by(Words.word_from.asc(), Words.word_to.asc()).all()

	return render_template("words/words.html", words=words_list)


@words.route("/word/add", methods=["GET", "POST"])
def word_add():
	form = WordForm()

	if form.validate_on_submit():
		word = Words()
		word.word_from = form.word_from.data
		word.word_to = form.word_to.data

		db.session.add(word)
		db.session.commit()

		flash("Palavra cadastrado com sucesso", "success")
		return redirect(url_for(".word_add"))

	return render_template("words/add.html", form=form)

@words.route("/word/delete/<int:id>")
def word_delete(id):
	word = Words.query.filter_by(id=id).first()
	db.session.delete(word)
	db.session.commit()

	return redirect(url_for(".list_words"))

@words.route("/change_description", methods=["GET", "POST"])
def change_description():
	

	if request.method == "POST":
		f = request.files['file_description']
		if f.filename == "":
			flash(message="É necessário informar uma planilha.",
			category="danger"
			)
			return render_template("change_description.html")

		if request.form["description"] == "":
			flash(message="É necessário informar o campo de descrição.",
			category="danger"
			)
			return render_template("change_description.html")

		if request.form["label"] == "":
			flash(message="É necessário informar o campo de marca.",
			category="danger"
			)
			return render_template("change_description.html")


		df = read_excel(f)
		columns = list(df.columns)

		if request.form["description"] not in columns:
			flash(message="O campo '"+request.form["description"]+"' não foi encontrado na planilha.",
			category="danger"
			)
			return render_template("change_description.html")

		if request.form["label"] not in columns:
			flash(message="O campo '"+request.form["label"]+"' não foi encontrado na planilha.",
			category="danger"
			)
			return render_template("change_description.html")

		df = validate_description(df, request.form["description"], request.form["label"])
		
		# SALVADO EXCEL 
		UPLOAD_FOLDER = os.path.join(current_app.config['UPLOAD_FOLDER'], "description.xlsx")
		df.to_excel(UPLOAD_FOLDER)

		return send_file(UPLOAD_FOLDER, as_attachment=True)	

	return render_template("change_description.html")