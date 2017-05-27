class OWLClass:
    temp = """name:{name} props:{props} attributes:{attributes}"""

    def __init__(self):
        self.props = []
        self.attributes = []
        self.name = None
        self.cls = None
        pass

    def __str__(self):
        return self.temp.format(name=self.name, props=self.props, attributes=self.attributes)

