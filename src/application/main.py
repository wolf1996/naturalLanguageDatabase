from neo4jrestclient.client import GraphDatabase
import keyring

import AppCore.nlpdatabase.nlp_interface as nlp
import configparser


def main():
    config = configparser.ConfigParser()
    config.read('config')
    inter = nlp.NLPInterface(config['DEFAULT']['syntaxnet_path'],
                             config['DEFAULT']['model_path'],
                             config['DEFAULT']['ignore_file_path'],
                             config['DEFAULT']['workdir'])
    username = config['DEFAULT']['neo4j_username']
    url = config['DEFAULT']['neo4j_url']
    inter.load_terasus()
    pss = keyring.get_password("neo4j", username)
    neo = GraphDatabase(url, username=username, password=pss)
    while True:
        try:
            # str = "Человек , рождённый [1952-05-02] , снявшийся в фильме ."
            str = "Актёр снимавшийся в фильме , снятом [2001-07-20] ."  # input(u"Введите запрос")
            # str = "Актёр , снявший фильм ." #на основании сущностей и классов в базе данных
            # str = "Режиссёр , снимавшийся в фильме ."
            # str = "Актёр снимавшийся в фильме , срежессированном [Quentin_Tarantino] ."
            # str = "Актёр снимавшийся в фильме , срежессированном человеком, родившимся  [1963-03-27]."
            print(inter.get_data(str)[0].lst())
            inter.simplify_data()
            for i in inter.result:
                print(i.lst())
            q = inter.get_cypher()[0]
        except Exception as ex:
            print("Parsing error")
            break
        print(q)
        print("\n###############################")
        res = neo.query(q=q)
        for i in res:
            for k in i:
                for j in k["data"].items():
                    print("{} {}".format(j[0], j[1]))
                print("###############################")

        break
    pass

if __name__ == "__main__":
    main()
