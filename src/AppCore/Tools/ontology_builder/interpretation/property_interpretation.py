from AppCore.Tools.ontology_builder.interpretation.base_interpretation import BaseImplementation


class PropertyInterpretation(BaseImplementation):
    def __init__(self, cls):
        super(__class__, self).__init__(cls)
        self.range = [i.__name__ for i in cls.range]
        self.domain = [i.__name__ for i in cls.domain]
