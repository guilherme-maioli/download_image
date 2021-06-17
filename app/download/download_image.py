import os
import requests 
import shutil 
import pandas as pd

from zipfile import ZipFile
from os.path import basename


def download_image_web(df, image_url, filename, directory):
	imagem_download = []
	for i in range(len(df)):

		url = str(df[image_url][i])
		file_name = str(df[filename][i])
		file_name =  os.path.join(directory, str(file_name) + ".jpg")
		r = requests.get(url, stream = True)

		if r.status_code == 200:
			imagem_download.append("SIM")
			r.raw.decode_intent = True
			with open(file_name, "wb") as f:
				shutil.copyfileobj(r.raw, f)
		else:
			imagem_download.append("NÃO")

	return imagem_download

def zip_folder(directory):
	
	dirName = directory

	# create a ZipFile object
	with ZipFile('images.zip', 'w') as zipObj:
	   # Iterate over all the files in directory
	   for folderName, subfolders, filenames in os.walk(dirName):
	       for filename in filenames:
	           #create complete filepath of file in directory
	           filePath = os.path.join(folderName, filename)
	           # Add file to zip
	           zipObj.write(filePath, basename(filePath))


def delete_all_files(directory):

	folder = directory
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))
