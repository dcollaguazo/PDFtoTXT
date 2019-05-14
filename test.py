import pandas as pd
import re
from datetime import datetime
import locale
import os


'''
Script that cleans the scraped dataframe from the sec page
'''
###########################################
###  CODE - 1: Removind outdated documents 
###########################################
# csv_filepath = 'enlaces_sec_test.csv'
# df = pd.read_csv(csv_filepath, header=0, keep_default_na=False)
# df_s = df.shift(-1)
# regex = re.compile('(PR-\\d{1,4})')
# idx_to_drop=[]
# # print(df['code'])

# for idx, r in df.iterrows():
# 	if str(df['code'][idx]) != 'nan' and str(df_s['code'][idx]) != 'nan':
# 		current_code = regex.search(df['code'][idx])
# 		next_code = regex.search(df_s['code'][idx])
# 		if current_code.group(1) == next_code.group(1):
# 			if idx+1 not in idx_to_drop:
# 				idx_to_drop.append(idx+1)
# df = df.drop(idx_to_drop)
# try:
# 	df = df.drop(columns=['Unnamed: 0'])
# except Exception as e:
# 	print(e)

# df.to_csv('enlaces_sec_cleaned.csv', index=0)

################################################
###  CODE - 2: striping the space from column
################################################
# csv_filepath = 'enlaces_sec_cleaned.csv'
# df = pd.read_csv(csv_filepath, header=0, keep_default_na=False)
# PR_code= 'PR-4681'
# df['code'] = df['code'].map(lambda x: x.strip())

# row = df.loc[df['code'] == PR_code]
# # print(row['date'].values)
# # my_date = df['date'][0].capitalize()
# locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
# my_date = 'abr'

# my_date = datetime.strptime(my_date,'%b')
# print(my_date)
################################################
###  CODE - 3: fixing dates
################################################
# csv_filepath = 'enlaces_sec_cleaned.csv'
# df = pd.read_csv(csv_filepath, header=0, keep_default_na=False)
# month_dict = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']

# for idx, r in df.iterrows():
# 	format_1 = re.match('(\\d{1,}) (\\w{1,3}) (\\d{1,4})', df['date'][idx])
# 	if format_1 != None:
# 		month = str(month_dict.index(format_1.group(2)) + 1)
# 		df['date'][idx] = format_1.group(3)[2:] + '/'  + month + '/' + format_1.group(1)
# for idx, r in df.iterrows():
# 	format_2 = re.match('(\\d{1,})-(\\w{1,})-(\\d{1,})', df['date'][idx])
# 	if format_2 != None:
# 		month_2 = str(month_dict.index(format_2.group(2).lower()) + 1)
# 		df['date'][idx] = format_2.group(3) + '/'  + month_2 + '/'  + format_2.group(1)

# df.to_csv('enlaces_sec_cleaned_date.csv', index=0)

################################################
###  CODE - 4: PDFMiner
################################################
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
# from cStringIO import StringIO

def pdf_to_text(pdfname):

    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    fp = open(pdfname, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()

    # Get text from StringIO
    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()

    return text
if __name__ == "__main__":
   text = pdf_to_text('C:\\Users\\DANIELACO\\PDFtoTXT\\pdf\\ProjectProposals\\Argentina. Loan 1914-OC-AR for the “Multiphase Program for the Development of Production Support Infrastructure in Entre Ríos – Phase I”. Closure of case file AR-MICI001-2010.pdf')
   print(text)
   print(type(text))