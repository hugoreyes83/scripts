from googletrans import Translator
import logging
import argparse

#setting up logging
LOG_FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format = LOG_FORMAT)

def init_translator():
    try:
        translator = Translator()
        return translator
    except:
        logging.info('could not initiate translator object, try installing module\
        with pip install googletrans')

def get_args():
    #setting up argparser
    parser = argparse.ArgumentParser(description='translate tool')
    parser.add_argument('--text',required=True)
    args = parser.parse_args()
    return args

def main():
    translate = init_translator()
    getargs = get_args()
    print(translate.translate(getargs.text,src='en',dest='es').text)

if __name__ == '__main__':
    main()
