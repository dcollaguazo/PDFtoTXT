import pandas as pd
import json
from langdetect import detect
import argparse



def detect_language(input):
    try:
        return detect(input)
    except Exception as e:
        return ''

def structure_detect_lang(file_path=None, encoding=None):
    df = pd.read_json(file_path, encoding=encoding)    
    df['contentLanguage'] = df['content'].apply(lambda x: detect_language(" ".join(x)) if len(" ".join(x)) > 0 else '')
    df.to_json(file_path, orient='records')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', help='Path to .json file that language need to be detected')
    parser.add_argument('--encoding', help='Encoding before open file')
    args = parser.parse_args()
    structure_detect_lang(args.filepath, args.encoding)