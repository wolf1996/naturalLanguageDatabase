from DatabaseLoader.data_loader.data_loader import TMDBLoader
from DatabaseLoader.owl_loader.owl_loader import OwlLoader

import configparser


def owl_test():
    config = configparser.ConfigParser()
    config.read('config')
    owl_loader = OwlLoader()
    owl_loader.open_file(config['DEFAULT']['owl_ontology'])
    # print(onto.classes)
    # cls = onto.classes[0]
    # print(cls.properties)
    # onto.subclasses()
    # print(onto.sync_reasoner())
    # print(onto.properties)
    # print(onto.properties[0].domain)
    # for i in onto.subclasses_of(onto.classes[4]):
    #    print(i)
    print(owl_loader.get_scheme())
    # owl_loader.make_instanse()
    # owl_loader.save()
    # owl_loader.remove_file()
    pass


def tmdb_test():
    config = configparser.ConfigParser()
    config.read('config')
    api_key = config['DEFAULT']['apikey']
    loader = TMDBLoader(api_key)
    mv = loader.get_movie(432517)
    print(mv.credits())
    print(mv.info()['production_countries'])
    print(mv.info())
    prsn = loader.get_person(71580)
    print(prsn.info())
    mvlist = loader.get_top_rated()
    print(mvlist['results'][0])


def tmdb_load_test():
    config = configparser.ConfigParser()
    config.read('config')
    api_key = config['DEFAULT']['apikey']
    loader = TMDBLoader(api_key)
    owl_loader = OwlLoader()
    owl_loader.open_file(config['DEFAULT']['owl_ontology'])
    mvlist = loader.get_top_rated()
    # mv, md = loader.get_movie(432517)
    # prsn, mp = loader.get_person(71580)
    # print(mv.credits())
    # print(mv.info())
    # print(prsn.info())
    # print(md.get_persons())
    # print(mvlist['results'][0])
    lst = []
    print("load list")
    for i in mvlist['results']:
        lst.append(i['id'])
    movies = dict()
    persons = dict()
    personid = set()
    countries = set()
    print("load movies {}".format(len(lst)))
    for ind, i in enumerate(lst):
        sup, mv = loader.get_movie(i)
        # print(sup.info())
        personid = personid.union(mv.get_persons())
        countries = countries.union(mv.get_country_prods())
        movies[i] = mv
        print(ind)
    print("load persons {}".format(len(personid)))
    for ind, i in enumerate(personid):
        _, person = loader.get_person(i)
        persons[i] = person
        print(ind)
    owl_loader.upload(movies, persons, countries)
    # owl_loader.remove_file()
    owl_loader.save()
    print(personid)
    print(movies)
    print(persons)


if __name__ == "__main__":
    # owl_test()
    # tmdb_test()
    tmdb_load_test()
