from AppCore.Tools.ontology_builder.class_description_manager import ClassDescriptionManager as Mgr
import configparser


def describer_test():
    config = configparser.ConfigParser()
    config.read('config')
    owl_file = config['DEFAULT']['owl_file']
    workdir = config['DEFAULT']['work_dir']
    manager = Mgr(workdir, owl_file)
    manager.process()
    pass


def load_onto():
    config = configparser.ConfigParser()
    config.read('config')
    pass


if __name__ == '__main__':
    describer_test()
    # load_onto()
    pass
