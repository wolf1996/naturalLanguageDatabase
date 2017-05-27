import os

from AppCore.Tools.ontology_builder.interpretation.class_interpretation import ClassInterpretation
from AppCore.Tools.ontology_builder.interpretation.property_interpretation import PropertyInterpretation
from DatabaseLoader.owl_loader.owl_loader import OwlLoader


class ClassDescriptionManager(object):
    def __init__(self, directory, owl):
        self.work_dir = directory
        self.class_work_dir = os.path.join(self.work_dir, 'classes')
        self.properties_work_dir = os.path.join(self.work_dir, 'properties')
        self.owl_file = owl
        self.owl = None

    @staticmethod
    def __generate_name(name):
        return "{}.json".format(name)

    def __create_file_descr_for_class(self, cls):
        fname = ClassDescriptionManager.__generate_name(cls)
        npath = os.path.join(self.class_work_dir, fname)
        file = open(npath, 'w')
        view = ClassInterpretation(cls)
        file.write(view.toJSON())

    def __create_file_descr_for_prperty(self, cls):
        fname = ClassDescriptionManager.__generate_name(cls)
        npath = os.path.join(self.properties_work_dir, fname)
        file = open(npath, 'w')
        view = PropertyInterpretation(cls)
        file.write(view.toJSON())

    def process(self):
        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)
            os.makedirs(self.class_work_dir)
            os.makedirs(self.properties_work_dir)
        owl_loader = OwlLoader()
        owl_loader.open_file(self.owl_file)
        self.owl = owl_loader.load()
        # self.owl.sync_reasoner()
        for i in self.owl.classes:
            self.__create_file_descr_for_class(i)
        for i in self.owl.properties:
            self.__create_file_descr_for_prperty(i)
