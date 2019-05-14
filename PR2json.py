#!C:\Users\DANIELACO\AppData\Local\Continuum\anaconda3\envs\pdf_to_txt\python.exe
# -*- coding: utf-8 -*-
from tika import parser
import pandas as pd
import os
import json
import re
from os import path, listdir
from _datetime import datetime
from LanguageDetector import LanguageDetector
import nltk.data
from PyPDF2 import PdfFileReader, PdfFileWriter


def formatPdf2Txt(filepath,sensitivity='private',id=""):
    file_name = './pdf/ProjectProposals/' + filepath
    now = datetime.utcnow() 
    fileType = "PR - Project Proposal"
    source = "http://sec.iadb.org/Site/Documents/ListDocBySeries.aspx?pCLS_ROWID=15&pOrgCode=IDB&pCode=PR"
    sensitivity = "public"
    df_date_lookup = pd.read_csv("enlaces_sec_cleaned_date.csv", keep_default_na=False)
    df_date_lookup['code'] = df_date_lookup['code'].map(lambda x: x.strip()[0:7]) 
    sourceDate = ""
    generatedDate =  now.strftime("%Y-%m-%dT%H:%M:%S%z") + now.strftime('.%f')[:4] + 'Z'
    PR_code = ""
    regex_PR_code = re.compile('(PR-\\d{1,4})')

    try:
        parsed = parser.from_file(file_name, xmlContent=False)
        parsed_txt = parsed["content"]
        str_len = len(parsed_txt)
        # Removing Table of Contents, etc.
        if(parsed_txt.find("Contents")!= -1):
            str_start = parsed_txt.find("Contents")
            parsed_txt = parsed_txt[str_start:str_len]

        # Search and removing References starting from the half of the document
        if(parsed_txt.find("References",int(str_len*.5),str_len)!= -1):
            str_end = parsed_txt.find("References",int(str_len*.5),str_len)  
            to_cut = str_len - str_end
            parsed_txt = parsed_txt[0:-to_cut]

        parsed_txt = re.sub(r"(?:https?|ftp)://[\w_-]+(?:\.[\w_-]+)+(?:[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?","", parsed_txt)
        parsed_txt = re.sub(r"-\n\n","",parsed_txt)
        parsed_txt = re.sub(r"-\n","",parsed_txt)
        # transforming all the text into a chunk of text by removing all breaks.
        # We will afterwards try to re-create the paragraphs
        parsed_txt = re.sub(r"\n"," ",parsed_txt)
        # removing extra spaces
        parsed_txt = re.sub(r"\s{2,}"," ",parsed_txt)
        #removing excesive punctuation
        parsed_txt = re.sub(r"\n(\.{3,})","\\1",parsed_txt)
        # trying to remove content of table of contents
        parsed_txt = re.sub(r"(\.{2,} \d{1,}) ([^.!?]*[.!?])","", parsed_txt)
        # creating paragraphs of 6 sentences - 6 was a random number
        parsed_txt = re.sub(r"(([^.!?]*[.!?]){1,6})","\\1\n",parsed_txt)
        
        PR_code = regex_PR_code.search(parsed_txt).group(1)
        row = df_date_lookup.loc[df_date_lookup['code'] == PR_code]
        sourceDate = row['date'].values[0]
        if sourceDate != '':
            sourceDate = datetime.strptime(sourceDate,'%y/%m/%d')
            sourceDate = datetime.strftime(sourceDate, '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        lang_det = LanguageDetector()    
        lang = lang_det.detect(parsed_txt)
        data = {"type": fileType,
                "employeeId": '',
                "source": source,
                "sensitivity": sensitivity,
                "sourceDate": sourceDate,
                "generatedDate": generatedDate,
                "tags": [PR_code],
                "content": parsed_txt,
                "language": lang
                }
        if not os.path.isdir('output'):
            os.mkdir('output')
        with open('output/PR/%s.json'%(PR_code + "_" + lang), 'w',encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)  

    except Exception as e:
        print("An exception occurred: ", e)

if __name__ == "__main__":
    for pdf in listdir('C:/Users/DANIELACO/PDFtoTXT/pdf/ProjectProposals/'):
        formatPdf2Txt(pdf)