"""
    OWL loader model
"""

import os
import pathlib
import random
import string

import owlready
from owlready import *

from DatabaseLoader.owl_loader.owl_class import OWLClass


class OwlLoader:
    """
        OWL loader class
    """

    def __init__(self):
        self.nfilename = None
        self.loaded = None
        self.onto = None
        self.loaded_movie = {}
        self.loaded_person = {}
        self.loaded_countries = {}
        self.loaded_genres = {}
        pass

    def open_file(self, filename):
        self.nfilename = self._file_name_generator()
        onto_url = pathlib.Path(os.path.abspath(filename)).as_uri()
        self.onto = owlready.get_ontology(onto_url)

    def load(self):
        self.loaded = self.onto.load()
        return self.loaded

    def get_scheme(self):
        lst = []
        for i in self.onto.classes:
            buf = OWLClass()
            buf.cls = i
            buf.name = str(i)
            lst.append(str(buf))
        return lst

    # def make_instanse(self):
    #    self.onto.classes[0]("pers1")
    #    pass

    def remove_file(self):
        os.remove(self.nfilename)

    def save(self):
        self.onto.save(self.nfilename)

    def add_genres(self, genre):
        return types.new_class(self._class_name_generator(str(genre)), (self.onto.Film,), kwds={"ontology": self.onto})

    def add_movie(self, movie):
        filmclass = self.onto.Film
        onto_genres = []
        for i in filmclass.descendant_subclasses():
            onto_genres.append(i)
        movie_genres = movie.genres
        movie_onto_classes = []
        for i in movie_genres:
            if i not in self.loaded_genres:
                genre = self.add_genres(i)
                movie_onto_classes.append(genre)
                self.loaded_genres[i] = genre
            else:
                genre = self.loaded_genres[i]
                movie_onto_classes.append(genre)
        print([str(i) for i in movie_genres])
        owl_film = filmclass(self._instance_name_generator(str(movie.name)), ontology=self.onto)
        owl_film.Name.append(movie.name)
        rel_date = movie.release_date
        owl_film.DateOfRelease.append(rel_date)
        for i in movie_onto_classes:
            owl_film.is_a.append(i)
        for i in movie.actors:
            actor = self.loaded_person[i]
            actor.is_a.append(self.onto.Actor)
        for i in movie.directors:
            director = self.loaded_person[i]
            director.is_a.append(self.onto.Director)
        return owl_film

    def _connect_props(self, movie):
        owl_movie = self.loaded_movie[movie[0]]
        movie = movie[1]
        for i in movie.actors:
            actor = self.loaded_person[i]
            owl_movie.InvolveAsActor.append(actor)
            actor.Acted.append(owl_movie)
        for i in movie.directors:
            director = self.loaded_person[i]
            owl_movie.InvolveAsDirector.append(director)
            director.Directed.append(owl_movie)
        for i in movie.country_prods:
            country = self.loaded_countries[i]
            owl_movie.ProductionCountries.append(country)
            country.Products.append(owl_movie)

    def make_connections(self, movies):
        for i in movies.items():
            self._connect_props(i)
        pass

    def add_person(self, person):
        personclass = self.onto.Person
        owl_person = personclass(self._instance_name_generator(person.name))
        owl_person.Name.append(person.name)
        owl_person.DateOfBirthday.append(person.birth)
        return owl_person

    def add_country(self, country):
        countryclass = self.onto.Country
        owl_country = countryclass(self._instance_name_generator(country.name))
        owl_country.Name.append(country.name)
        return owl_country

    def upload(self, movies, persons, countries):
        print("creating countries")
        for i in countries:
            owl_country = self.add_country(i)
            self.loaded_countries[i] = owl_country
            pass
        print("creating persons")
        for i in persons.items():
            owl_person = self.add_person(i[1])
            self.loaded_person[i[0]] = owl_person
        print("creating movies")
        for i in movies.items():
            movie_owl = self.add_movie(i[1])
            self.loaded_movie[i[0]] = movie_owl
        print("creating connections")
        self.make_connections(movies)
        print("finish")
        pass

    def reasoning(self):

        pass

    @staticmethod
    def _file_name_generator(n=10):
        name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
        return "{}.xml".format(name)

    @staticmethod
    def get_genre(genrename, genrelist):
        for i in genrelist:
            if str(i) == genrename:
                return i

    @staticmethod
    def _class_name_generator(basename, n=3):
        bname = "".join(filter(str.isalpha, basename))
        newname = "{}OntologyClass".format(bname)
        newname += "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
        print(newname)
        return newname

    @staticmethod
    def _instance_name_generator(basename, n=3):
        bname = "".join(filter(str.isalpha, basename))
        newname = "{}OntologyInstance".format(bname)
        newname += "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
        print(newname)
        return newname
