import json

import pymorphy2


class IgnoreManager:
    morph = pymorphy2.MorphAnalyzer()

    def __init__(self, path):
        with open(path, 'r') as ignorefile:
            ifile = json.load(ignorefile)
            self.ignored_words = ifile['ignore']

    def __punctuation_ignore(self, word_prsd):
        return 'PNCT' in word_prsd.tag

    def __words_ignore(self, word_prsd):
        return word_prsd.normal_form in self.ignored_words

    def __preps_ignore(self, word_prsd):
        return 'PREP' in word_prsd.tag

    def check_ignore(self, word):
        parsed_word = IgnoreManager.morph.parse(word)[0]
        if self.__words_ignore(parsed_word):
            return True
        if self.__preps_ignore(parsed_word):
            return True
        if self.__punctuation_ignore(parsed_word):
            return True
        return False

    def check_ignore_parsed(self, parsed_word):
        if self.__words_ignore(parsed_word):
            return True
        if self.__preps_ignore(parsed_word):
            return True
        if self.__punctuation_ignore(parsed_word):
            return True
        return False

