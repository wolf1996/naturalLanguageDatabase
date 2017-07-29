import sys
from PyQt4 import QtCore, QtGui
from application.interface import Ui_MainWindow
from neo4jrestclient.client import GraphDatabase
import keyring

import AppCore.nlpdatabase.nlp_interface as nlp
import configparser



class IFace(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(IFace, self).__init__(parent)
        self.setupUi(self)
        self.star_button.clicked.connect(self.process)
        config = configparser.ConfigParser()
        config.read('config')
        self.inter = nlp.NLPInterface(config['DEFAULT']['syntaxnet_path'],
                                 config['DEFAULT']['model_path'],
                                 config['DEFAULT']['ignore_file_path'], config['DEFAULT']['workdir'])
        username = config['DEFAULT']['neo4j_username']
        url = config['DEFAULT']['neo4j_url']
        self.inter.load_terasus()
        pss = keyring.get_password("neo4j", username)
        self.neo = GraphDatabase(url, username=username, password=pss)

    def process(self):
        inp = self.lineEdit.text()
        result = ''
        try:
            #str = "Человек , рождённый [1952-05-02] , снявшийся в фильме ."
            #str = "Актёр снимавшийся в фильме , снятом [2001-07-20] ."#input(u"Введите запрос")
            #str = "Актёр , снявший фильм ." #на основании сущностей и классов в базе данных
            #str = "Режиссёр , снимавшийся в фильме ."
            #str = "Актёр снимавшийся в фильме , срежессированном [Quentin_Tarantino] ."
            #str = "Актёр снимавшийся в фильме , срежессированном человеком, родившимся  [1963-03-27]."
            self.inter.get_data(inp)
            for i in self.result:
                print(i.lst())
            self.inter.simplify_data()
            for i in self.result:
                print(i.lst())
            q = self.inter.get_cypher()[0]
        except Exception as ex:
            result += "Parsing error\n"
        result += (q+'\n')
        result += ("\n###############################\n")
        res = self.neo.query(q=q)
        for i in res:
            for k in i:
                for j in k["data"].items():
                    result+="{} {}\n".format(j[0], j[1])
                result+="###############################\n"
        self.raw_output.setText(result)
        pass


def start():
    app = QtGui.QApplication(sys.argv)
    form = IFace()
    form.show()
    app.exec()
    pass

if __name__ == '__main__':
    start()