""""
    Main interface class to database 
"""

from syntax_net_interface.syntax_net import SyntaxNet
from conllu.parser import parse_tree
import re

class NLPInterface:
    """
        interface to databse
    """
    def __init__(self, syntaxnetwdir, syntaxnetmodel, database, owlfile):
        """
        Database interface constructor
        :param syntaxnetwdir: 
            working dir of syntaxnet
        :param syntaxnetmodel: 
            syntaxnet pretrained model 
        :param database: 
            url to Neo4j dtabase
        :param owlfile:
            semantic net file
        """
        self.syntaxnet_working_dir = syntaxnetwdir
        self.database = database
        self.owlfile = owlfile
        self.syntaxnet_model = syntaxnetmodel
        self.syntaxnet_interface = SyntaxNet(self.syntaxnet_working_dir, self.syntaxnet_model)
        pass

    def get_data(self, query):
        """
        get some data from database
        :param query: 
            string on russian 
        :return: 
            json with data from database
        """
        conll = self.syntaxnet_interface.parse(query)
        data = re.sub(r" +", r"\t", conll)
        result = parse_tree(data)
        return result


def test():
    """
        some fast tests
    :return: 
        None
    """
    inter = NLPInterface("/home/ksg/disk_d/labs_2017/diploma/syntaxnet/models/syntaxnet", \
                         "/home/ksg/disk_d/labs_2017/diploma/pretrained_model/Russian",
                         None, None)
    print(inter.get_data(u"Фильм , снятый в 1998 году ."))
    pass

if __name__ == '__main__':
    test()
