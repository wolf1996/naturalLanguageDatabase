from neo4jrestclient.client import GraphDatabase
import keyring
import configparser

from AppCore.Tools.ontology_loader.ontology_loader import OntologyLoader
from DatabaseLoader.owl_loader.owl_loader import OwlLoader


def test_load():
    config = configparser.ConfigParser()
    config.read('config')
    username = config['DEFAULT']['neo4j_username']
    url = config['DEFAULT']['neo4j_url']
    onto_file = config['DEFAULT']['owl_file']
    pss = keyring.get_password("neo4j", username)
    neo = GraphDatabase(url, username=username, password=pss)
    owl_loader = OwlLoader()
    owl_loader.open_file(onto_file)
    ontology = owl_loader.load()
    ont_loader = OntologyLoader(ontology, neo)
    ont_loader.load_classes()


if __name__ == '__main__':
    test_load()
