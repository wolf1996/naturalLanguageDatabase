import re
import string

import pymorphy2


class InvalidStemError(Exception):
    def __init__(self, error_name):
        self.error_name = error_name
    pass


class MyTree:
    mrph = pymorphy2.MorphAnalyzer()

    def __init__(self, tree, terasus, ignore_manager):
        self.terasus = terasus
        self.ignore_manager = ignore_manager
        self.name = tree.data['form']
        self.children = [MyTree(i,terasus,ignore_manager) for i in tree.children]
        self.system_name = None
        pass

    def lst(self):
        buf = [i.lst() for i in self.children]
        if buf:
            return [self.name, buf]
        else:
            return [self.name, ]

    def normalize_tree(self):
        parsed_name = MyTree.mrph.parse(self.name)[0]
        self.name = parsed_name.normal_form
        if self.ignore_manager.check_ignore_parsed(parsed_name):
            return False
        if not re.match("\[(.*)\]", self.name):
            if self.name in self.terasus.terasus:
                self.system_name = self.terasus.terasus[self.name]
            else:
                raise InvalidStemError(self.name)
        self.children = [i for i in self.children if i.normalize_tree()]
        return True
