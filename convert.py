from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from os import path, listdir
import io
import sys, getopt

def convert():

    for pdf in listdir('./pdfs'):
        text = convert_to_text('./pdfs/' + pdf)
        txt_file_name = pdf[0:-4]
        with open('./txts/' + txt_file_name + ".txt", "w", encoding="utf-8") as f:
            f.write(text)
            f.close()
        

def convert_to_text(fname):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
    fp = open(fname, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


if __name__ == '__main__':
    convert()
 