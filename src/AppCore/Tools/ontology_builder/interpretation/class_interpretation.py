from AppCore.Tools.ontology_builder.interpretation.base_interpretation import BaseImplementation


class ClassInterpretation(BaseImplementation):
    def __init__(self, cls):
        super(__class__, self).__init__(cls)
        self.subclass_of = [i.__name__ for i in cls.is_a]
