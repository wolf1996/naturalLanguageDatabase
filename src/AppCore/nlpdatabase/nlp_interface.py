""""
    Main interface class to database 
"""

import re

from AppCore.nlpdatabase.syntax_net_interface.syntax_net import SyntaxNet
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

    def __process_data_property(self, rel, node):
        concr = self.__get_concrete(node)
        rel.range = [self.__process(i) for i in node.children]
        rel.range.append(concr)
        pass

    def __process_relation(self, rel, node):
        rel.range = [self.__process(i) for i in node.children]
        pass

    def __process_children(self, cont, child):
        rel = RelationContainer()
        node_interpretation = self.terasus.terasus[child.name]
        rel.is_a = node_interpretation
        if not node_interpretation[0].type == 'property':
            return None
        prop = self.terasus.classes[node_interpretation[0].system_name]
        if 'str' in prop.range:
            self.__process_data_property(rel, child)
            cont.data_properties.append(rel)
        else:
            self.__process_relation(rel, child)
            cont.data_relations.append(rel)

    def __process(self, node, n=0, key=None):
        if key is None:
            key = self.__get_key()
        cont = NodeContainer(self.terasus, self.__get_key)
        if re.match("\[(.*)\]", node.name):
            cont.data_properties_resolved['Name'] = node.name[1:-1]
        else:
            cont.is_a = self.terasus.terasus[node.name]
        for i in node.children:
            self.__process_children(cont, i)
            pass
        return cont

    def get_cypher(self):
        res = []
        for i in self.result:
            res.append(self.__process(i))
        cyph = []
        for i in res:
            i.id = self.__get_key()
            cyph.append((i.get_cypher()+'\n return distinct {}'.format(i.id)))
        self.current_key = "a"
        return cyph
