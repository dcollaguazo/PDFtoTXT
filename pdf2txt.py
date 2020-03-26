#!C:\Users\DANIELACO\AppData\Local\Continuum\anaconda3\envs\pdf_to_txt\python.exe
# -*- coding: utf-8 -*-
from tika import parser
import os
import re
from os import path, listdir
from englishDetector import EnglishDetector
import nltk.data
from PyPDF2 import PdfFileReader, PdfFileWriter


def formatPdf2Txt(filepath,sensitivity='private',id=""):
    file_name = './abstractive summarization literature/papers_in_state_of_art/' + filepath
    # current_pdf = PdfFileReader(file_name)
    # parsed_txt = ''
    
    try:
        # for i in range(current_pdf.numPages):
        #     parsed_txt = parsed_txt + current_pdf.getPage(i).extractText()
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
        # removing extra spaces
        parsed_txt = re.sub(r"\s{2,}"," ",parsed_txt)
        # removing breaks with words
        parsed_txt = re.sub(r"-\n","",parsed_txt)
        # removing extra breaks
        parsed_txt = re.sub(r"\n"," ",parsed_txt)
        
        #removing excesive punctuation
        # parsed_txt = re.sub(r"\n(\.{3,})","\\1",parsed_txt)
        # trying to remove content of table of contents
        # parsed_txt = re.sub(r"(\.{2,} \d{1,}) ([^.!?]*[.!?])","", parsed_txt)
        # parsed_txt = re.sub(r" (\.{3,})","", parsed_txt)
        # creating paragraphs of 6 sentences - 6 was a random number
        # parsed_txt = re.sub(r"(([^.!?]*[.!?]){1,6})","\\1\n",parsed_txt)
        
        eng_det = EnglishDetector()
        engBoolean= eng_det.is_english(parsed_txt)

        if engBoolean:
            with open('./txtAbstractiveSummarization/papers_in_state_of_art/' + filepath[0:-4] + ".txt", "w", encoding="utf-8") as f:
                f.write(parsed_txt)
                f.close()
        else:
            print("Document %s given is not in english."%filepath)
    except Exception as e:
        print("An exception occurred: ", e)

if __name__ == "__main__":
    for pdf in listdir('C:/Users/DANIELACO/PDFtoTXT/abstractive summarization literature/papers_in_state_of_art/'):
        formatPdf2Txt(pdf)