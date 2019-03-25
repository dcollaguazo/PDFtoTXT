from os import path, listdir
import io
import sys, getopt

def cleanTXT():
    for txt in listdir('./txt'):
        text = txt
        # text = convert_to_text('./pdfs/' + pdf)
        # txt_file_name = pdf[0:-4]
        # with open('./txts/' + txt_file_name + ".txt", "w", encoding="utf-8") as f:
        #     f.write(text)
        #     f.close()

if __name__ == '__main__':
    cleanTXT()
 