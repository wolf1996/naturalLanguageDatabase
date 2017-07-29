""""
    Main interface class to database 
"""

import re

from syntax_net_interface.syntax_net import SyntaxNet
from conllu.parser import parse_tree
from AppCore.nlpdatabase.my_syntax_tree.my_tree import MyTree
from AppCore.nlpdatabase.terasus.my_terasus import MyTerasus
from AppCore.nlpdatabase.my_syntax_tree.ignore_manager import IgnoreManager
from AppCore.nlpdatabase.my_syntax_tree.node_container import NodeContainer
from AppCore.nlpdatabase.my_syntax_tree.relation_container import RelationContainer


class NLPInterface:
    """
        interface to databse
    """

    def __init__(self, syntaxnetwdir, syntaxnetmodel, json_ignore_path, workdir):
        """
        Database interface constructor
        :param syntaxnetwdir: 
            working dir of syntaxnet
        :param syntaxnetmodel: 
            syntaxnet pretrained model 
        :param json_ignore_path:
            path to ignore file
        :param workdir:
            path to directory with classes and properties description
        """
        self.syntaxnet_working_dir = syntaxnetwdir
        self.ignore_manager = IgnoreManager(json_ignore_path)
        self.workdir = workdir
        self.syntaxnet_model = syntaxnetmodel
        self.syntaxnet_interface = SyntaxNet(self.syntaxnet_working_dir, self.syntaxnet_model)
        self.terasus = MyTerasus(self.workdir)
        self.result = None
        self.current_key = "a"
        pass

    def __get_key(self):
        self.current_key += "a"
        return self.current_key

    def load_terasus(self):
        self.terasus.load()
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
        self.result = parse_tree(data)
        self.result = [MyTree(i, self.terasus, self.ignore_manager) for i in self.result]
        return self.result

    def simplify_data(self):
        return [i.normalize_tree() for i in self.result]

    def __get_concrete(self, node):
        for i in node.children:
            if re.match("\[(.*)\]", i.name):
                return i.name[1:-1]

    def __process_property(self, node, sysnode, key, n):
        range = self.terasus.classes[sysnode.system_name].range
        if 'str' in range:
            return "WHERE ({}.{} = {})\n".format(key, sysnode.system_name, self.__get_concrete(node))
        pass

    def __process_children(self, node, key, n):
        node_interpretation = self.terasus.terasus[node.name]
        for i in node_interpretation:
            if i.type == 'property':
                return  self.__process_property(node, i, key, n)

    def __create_base(self, key, node):
        bufkey = self.__get_key()
        res = "MATCH({}) - [: is_a * 0..]->({})\n".format(key, bufkey)
        res += "WHERE "
        res += '{}.system_name in '.format(bufkey)
        types = [i.system_name for i in self.terasus.terasus[node.name]]
        res += str(types)
        res += '\n'
        return res

    def __process(self, node, n=0, key=None):
        if key is None:
            key = self.__get_key()
        cypher = "MATCH ({})\n".format(key)
        if re.match("\[(.*)\]", node.name):
            cypher += "n.Name={}".format(self.name[1:-1])
        else:
            cypher += self.__create_base(key, node)
        for i in node.children:
            cypher += self.__process_children(i, key,n+1)
            pass
        if n == 0:
            cypher += ("return {}".format(key))
        return cypher

    def get_cypher(self):
        res = []
        for i in self.result:
            res.append(self.__process(i))
        return res
