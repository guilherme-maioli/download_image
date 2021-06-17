import pandas as pd 
from app.models import Words
from app.words.number import word_after_number, word_before_number, unidades




def is_number(value):
    value = value.lower()
    if not value.strip().replace('kg', '').replace('ml', '').replace('gr', '').replace('gs', '').replace('g', '').replace('l', '').replace('lts', '').replace(',', '').replace('.', '').isdigit():
        return False
    else:
        return True

def validate_description(df, description, label):
	## colunas já existentes
	df[description] = df[description].map(str).fillna("")
	df[label] = df[label].map(str).fillna("")

	## criando novas colunas
	df['new_description'] = df[description].str.lower()
	df['new_label'] = df[label].str.lower()

	df['new_description'] = arruma_unidade_medida(df, 'new_description')
	df['new_description'] = column_organize(df, 'new_description')
	df['new_label'] = column_organize(df, 'new_label')

	return df


def arruma_unidade_medida(df, column):
	'''
	junta número e unidade, exemplo: 1 L -> 1L
	'''
	correct = []
	for i in range(len(df)):
		# remove espaço do começo e final
		df[column][i] = df[column][i].strip() 

		x = df[column][i].split(" ")

		for i2 in range(len(x)):
			x[i2] = x[i2].strip()

			# se for o primeiro pula
			if i2 == 0:
				continue
			if x[i2] in unidades:
				# coloca unidade para L
				if x[i2] in ["l", "lts", "litro", "litros"]:
					x[i2] = "L"
				elif x[i2] in ["gr", "gs", "grs"]:
					x[i2] = "g"

				if is_number(x[i2-1]):
					x[i2] = x[i2-1]+x[i2]
					x.pop(i2-1)

		sDesc = ""
		for i2 in range(len(x)):
			sDesc = sDesc + x[i2] + " "

		correct.append(sDesc.strip())

	return correct
					



def column_organize(df, column):

	description = []

	for i in range(len(df)):
		# remove espaço do começo e final
		df[column][i] = df[column][i].strip() 
		
		x = df[column][i].split(" ")
		correct = []
		for i2 in range(len(x)):
			x[i2] = x[i2].strip()
			
			word = Words.query.filter_by(word_from=x[i2]).first()
			if word is not None:
				x[i2] = word.word_to + "|"
			
			# SE É NÚMERO	
			if is_number(x[i2]):
				if i2 <= len(x)-2:
					if x[i2+1] in word_after_number:
						x[i2] = x[i2] + "|"
				
				if i2 > 0:
					if x[i2-1] in word_before_number:
						x[i2] = x[i2] + "|"
		
			correct.append(x[i2])

		sDesc = ""
		sDesc_fim = ""
		for i3 in range(len(correct)):
			if correct[i3][-1] == "|":
				correct[i3] = correct[i3][0:len(correct[i3]) - 1]
				sDesc = sDesc + correct[i3] + " "
			elif is_number(correct[i3]):
				sDesc_fim = " - " + correct[i3]
			else:
				correct[i3] = correct[i3].capitalize()
				sDesc = sDesc + correct[i3] + " "
		description.append(sDesc.strip() + sDesc_fim)
			
	return description




