"""
    Class to load and normalize data from tmdb
"""

import tmdbsimple

from DatabaseLoader.data_loader.data_models import *


class TMDBLoader:
    """
        Class to load films from TMDB
    """

    def __init__(self, apikey):
        self.apikey = apikey
        pass

    def get_movie(self, tmdbid):
        tmdbsimple.API_KEY = self.apikey
        movie = tmdbsimple.Movies(tmdbid)
        movie_inf = movie.info()
        movie_credits = movie.credits()
        my_mv_data = Movie()
        my_mv_data.set_info(movie_inf)
        my_mv_data.set_credits(movie_credits)
        return movie, my_mv_data

    def get_person(self, tmdbid):
        tmdbsimple.API_KEY = self.apikey
        person = tmdbsimple.People(tmdbid)
        person_info = person.info()
        prsn = Person()
        prsn.set_info(person_info)
        return person, prsn

    def get_top_rated(self, **kwargs):
        tmdbsimple.API_KEY = self.apikey
        return tmdbsimple.Movies().top_rated(kwargs=kwargs)


def main():
    pass

if __name__ == '__main__':
    main()
