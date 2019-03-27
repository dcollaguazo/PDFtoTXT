from tika import parser
import os
import re
from os import path, listdir
from englishDetector import EnglishDetector
import nltk.data


def formatPdf2Txt(filepath,sensitivity='private',id=""):
    file_name = './pdf/' + filepath
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    try:
        parsed = parser.from_file(file_name, xmlContent=False) 
        parsed_txt = parsed["content"]
        parsed_txt = re.sub(r"-\n\n","",parsed_txt)
        parsed_txt = re.sub(r"-\n","",parsed_txt)
        parsed_txt = re.sub(r"\n{2,}","\n",parsed_txt)
        # parsed_txt = re.sub(r"\s{2,}"," ",parsed_txt)
        # parsed_txt = re.sub(r"(([^.!?]*[.!?]){1,5})","\\1\n",parsed_txt)

        # parsed_txt = '\n'.join(tokenizer.tokenize(parsed_txt))

        eng_det = EnglishDetector()
        engBoolean= eng_det.is_english(parsed_txt)

        if engBoolean:
            with open('./txt/' + filepath + ".txt", "w", encoding="utf-8") as f:
                f.write(parsed_txt)
                f.close()
        else:
            print("Document %s given is not in english."%filepath)
    except:
        print("An exception occurred")

if __name__ == "__main__":
    for pdf in listdir('C:/Users/DANIELACO/PDFtoTXT/pdf'):
        formatPdf2Txt(pdf)