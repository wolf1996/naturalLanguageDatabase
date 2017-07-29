import configparser

from AppCore.nlpdatabase.nlp_interface import NLPInterface

def test():
    """
        some fast tests
    :return: 
        None
    """
    config = configparser.ConfigParser()
    config.read('config')
    print(config)
    inter = NLPInterface(config['DEFAULT']['syntaxnet_path'],
                         config['DEFAULT']['model_path'],
                         config['DEFAULT']['ignore_file_path'],
                         config['DEFAULT']['workdir'])
    inter.load_terasus()
    inter.get_data(u"Фильм , снятый  [2001-07-20] .")
    #inter.get_data(u"Актёр участвовавший в фильме , снятом в [2001-07-20] .")
    #inter.get_data(u"Актёр участвовавший в [TheTitanic] , снятом в [2001-07-20] .")
    simplified_data = inter.simplify_data()
    for i in inter.result:
        print(i.lst())
    for i in inter.get_cypher():
        print(i)
    #dt = inter.get_data(u"Актёр участвовавший в фильме , снятом в [01-01-1998] .")
    #for i in dt:
    #    print(i.lst())
    #for i in dt:
    #    i.normalise_tree()
    #    print(i.lst())
    pass


if __name__ == '__main__':
    test()