from . import download

from pandas import read_excel
from datetime import datetime

from flask import render_template, request, flash, send_file, url_for, redirect
from app.download.download_image import download_image_web, zip_folder, delete_all_files
import os
from flask import current_app


@download.route("/download", methods=["GET", "POST"])
def download_image():

	if request.method == "POST":
		f = request.files['image_file']
		if f.filename == "":
			flash(message="É necessário informar uma planilha.",
			category="danger"
			)
			return render_template("download_image.html")

		if request.form["image_url"] == "":
			flash(message="É necessário informar um campo de URL.",
			category="danger"
			)
			return render_template("download_image.html")

		if request.form["image_name"] == "":
			flash(message="É necessário informar um campo de renomeação da imagem.",
			category="danger"
			)
			return render_template("download_image.html")


		df = read_excel(f)
		columns = list(df.columns)
		image_url = request.form["image_url"]
		image_name = request.form["image_name"]

		if image_url not in columns:
			flash(message="O campo '"+image_url+"' não foi encontrado na planilha.", category="danger")
			return render_template("download_image.html")
		
		if image_name not in columns:
			flash(message="O campo '"+image_name+"' não foi encontrado na planilha.", category="danger")
			return render_template("download_image.html")

		if len(df) == 0:
			flash(message="Não existe registros na planilha.", category="danger")
			return render_template("download_image.html")

		UPLOAD_FOLDER = os.path.join(current_app.config['UPLOAD_FOLDER'], "auxiliar.xlsx")	
		df.to_excel(UPLOAD_FOLDER)


		filename_now = datetime.now().strftime('%Y%m%d_%H%M%S')
		
		return redirect(url_for(".download_image_file", 
								filename=filename_now, 
								image_url=image_url,
								image_name=image_name
								)
						)
		
	return render_template("download_image.html")


@download.route("/download/<filename>/<image_url>/<image_name>")
def download_image_file(filename, image_url, image_name):

	try:
		UPLOAD_FOLDER = os.path.join(current_app.config['UPLOAD_FOLDER'], "auxiliar.xlsx")
		#print("Carregando excel auxiliar: "+ UPLOAD_FOLDER)
		df = read_excel(UPLOAD_FOLDER)
		
		UPLOAD_FOLDER = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)		
		## CRIANDO DIRETORIO
		if os.path.exists(UPLOAD_FOLDER):
			flash(message="Diretório já existente. Tente novamente...", category="danger")
			return render_template("download_image.html")
		else:
			#print("CRIANDO DIR: "+UPLOAD_FOLDER)
			os.mkdir(UPLOAD_FOLDER)

		## download das imagens
		#print("BAIXANDO IMAGEM: "+ UPLOAD_FOLDER)
		df["baixou?"] = download_image_web( df, 
											image_url, 
											image_name, 
											UPLOAD_FOLDER
										)

		
		UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, "imagens.xlsx")
		#print("Salvado excel: "+UPLOAD_FOLDER)
		df.to_excel(UPLOAD_FOLDER)

		## zipando os arquivos
		UPLOAD_FOLDER = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
		#print("Zipando pasta: "+UPLOAD_FOLDER)   	
		zip_folder(UPLOAD_FOLDER)

		## deletando arquivos da pasta
		#print("deletando: "+current_app.config['UPLOAD_FOLDER']) 
		delete_all_files(current_app.config['UPLOAD_FOLDER'])

		# download arquivo	
		UPLOAD_FOLDER = os.path.dirname(current_app.config['UPLOAD_FOLDER'])

		path = os.path.join(UPLOAD_FOLDER, "images.zip")
	
	except:
		delete_all_files(current_app.config['UPLOAD_FOLDER'])
	
	finally:
		return send_file(path, as_attachment=True)

