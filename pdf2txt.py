from tika import parser
import os
from os import path, listdir
from englishDetector import EnglishDetector


def formatPdf2Txt(filepath,sensitivity='private',id=""):
    file_name = './pdf/' + filepath
    try:
        parsed = parser.from_file(file_name, xmlContent=False) 
        eng_det = EnglishDetector()
        engBoolean= eng_det.is_english(parsed["content"])

        if engBoolean:
            with open('./txt/' + filepath + ".txt", "w", encoding="utf-8") as f:
                f.write(parsed["content"])
                f.close()
        else:
            print("Document %s given is not in english."%filepath)
    except:
        print("An exception occurred")

if __name__ == "__main__":
    for pdf in listdir('C:/Users/DANIELACO/PDFtoTXT/pdf'):
        formatPdf2Txt(pdf)