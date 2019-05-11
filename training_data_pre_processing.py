
"""Library for pre process labeled twitter sentiment data."""
import re

import nltk
from nltk.corpus import stopwords

import logging
import csv


class TrainingData:
    """Pre process training data."""

    def retrieve_train_test_data(self, csv_path, preview_row_count=20, test_data_size=100, training_data_size=1000):
        """Read in data from the csv path given into pandas and return training and test data."""
        training_data = []
        testing_data = []
        with open(csv_path, encoding = "ISO-8859-1") as file: 
            reader = csv.reader(file)
            while True: 
                try: 
                    row = next(reader)
                    row[-1] = self.sanitize_text(row[-1])
                    if training_data_size > 0:
                        training_data.append((row[0],row[-1].split(' ')))
                        training_data_size -= 1
                    elif test_data_size > 0: 
                        testing_data.append((row[0],row[-1].split(' ')))
                        test_data_size -= 1
                    else:
                        break
                except Exception as e:
                    logging.error(e)
        logging.info("Created training data of size "+str(len(training_data))+" and test data of size " + str(len(testing_data))) 
        return training_data, testing_data


    def sanitize_text(self, detail):
        # Step 1 lowercase the detail text
        detail = detail.lower()
        logging.debug("Starting detail text: " + detail)
        detail = self.translate_twitter_user_to_generic(detail)
        logging.debug("After translating user name: " + detail)
        detail = self.filter_url(detail)
        logging.debug("After removing any url: " + detail)
        detail = self.trim_excess_trailing_chars(detail)
        logging.debug("After word trimming: " + detail)
        detail = self.remove_punctuation(detail)
        logging.debug("After removing puctuations: "+ detail)
        detail = self.filter_stop_and_non_english_words(detail)
        logging.debug("After filtering stop and non english words: " + detail)
        detail = self.translate_hash_tag(detail)
        return detail


    def translate_twitter_user_to_generic(self,detail):
        detail = re.sub("@([A-Za-z0-9_]+)", "at_user", detail)
        return detail


    def translate_hash_tag(self,detail):
        return re.sub("#", "", detail)


    def filter_url(self,detail):
        return re.sub(r'http\S+', '', detail)


    def filter_stop_and_non_english_words(self,detail):
        stop_words = self.retrieve_stop_words()
        filtered_detail = []
        for word in detail.split(' '):
            if word not in stop_words and self.is_english_word(word):
                filtered_detail.append(word)
        return ' '.join(filtered_detail)


    def remove_punctuation(self,detail):
        return re.sub(r'[^\w\s]','',detail)


    def is_hash_or_user(self,word):
        return word == "at_user" or (len(word)>0 and word[0] == '#')


    # Checks for enlish word and not translated user name or hash tag
    def is_english_word(self,word):
        return word in self.english_words or self.is_hash_or_user(word)


    def trim_excess_trailing_chars(self,detail):
        return re.sub(r'(.)\1+', r'\1', detail)


    def retrieve_stop_words(self):
        count = 2
        while count > 0:
            try:
                return set(stopwords.words('english'))
            except Exception as e:
                print(e)
                print("Dowloading new set of stop words")
                nltk.download('stopwords')
            finally:
                count -= 1
        return None
    def __init__(self,*args,**kwargs):
        logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s', level=logging.INFO)
        logging.info("Logging started")
        try:
            self.english_words = set(nltk.corpus.words.words())
        except Exception as e:
            print(e)
            print("Downloading set of words")
            nltk.download('words')
