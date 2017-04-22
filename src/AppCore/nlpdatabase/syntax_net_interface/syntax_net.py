"""
    module to use syntaxnet
    from python
"""

import subprocess
import os

from .exceptions import *

class SyntaxNet:
    """
        interface to syntaxnet
    """
    def __init__(self, script_directory, model):
        """
        :param script_directory: 
            working dir of syntaxnet
            (/models/syntaxnet)
        :param model: 
            path to model 
        """
        self.script_directory = script_directory
        self.model = model

    def __apply_syntaxnet(self, query):
        """
            parse value using syntaxnet 
            :param query:
            query to parse
            :return: 
            error and stdout
        """
        class_directory = os.path.dirname(__file__)
        path = os.path.join(class_directory, "bash/parse.sh")
        cmd = [path, self.script_directory, self.model, query]
        print(cmd)
        parser = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        parser.wait()
        out = parser.stdout.read()
        err = parser.stderr.read()
        return out, err

    def parse(self, query):
        """
        parse value using syntaxnet 
        :param query:
         query to parse
        :return: 
         error and stdout
        """
        out, err = self.__apply_syntaxnet(query)
        if len(out) == 0:
            raise SyntaxNetError(err)
        return out.decode("utf-8")
