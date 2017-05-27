class Thing:
    def __init__(self):
        self.name = None

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class Person(Thing):
    def __init__(self):
        super().__init__()
        self.birth = None

    def set_info(self, info):
        self.name = info["name"]
        self.birth = info["birthday"]
        pass


class Country(Thing):
    def __init__(self):
        super().__init__()


class Movie(Thing):
    def __init__(self):
        super().__init__()
        self.name = None
        self.release_date = None
        self.actors = []
        self.directors = []
        self.country_prods = []
        self.genres = []

    def _parse_countries(self, countries):
        for i in countries:
            cntry = Country()
            cntry.name = i['name']
            self.country_prods.append(cntry)

    def _parse_genres(self, genres):
        for i in genres:
            gnr = Genre()
            gnr.name = i['name']
            self.genres.append(gnr)

    def _parse_actors(self, actors):
        for i in actors:
            self.actors.append(i['id'])
        pass

    def _parse_crew(self, crew):
        for i in crew:
            if i['job'] == 'Director':
                self.directors.append(i['id'])
        pass

    def set_info(self, info):
        self.name = info['original_title']
        self.release_date = info['release_date']
        self._parse_countries(info['production_countries'])
        self._parse_genres(info['genres'])

    def set_credits(self, credit):
        self._parse_actors(credit['cast'])
        self._parse_crew(credit['crew'])
        pass

    def get_persons(self):
        return set(self.actors).union(set(self.directors))

    def get_country_prods(self):
        return set(self.country_prods)

    def get_genres(self):
        return set(self.genres)


class Genre(Thing):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return self.name
