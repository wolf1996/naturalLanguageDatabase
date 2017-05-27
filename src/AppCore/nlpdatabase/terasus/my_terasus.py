import os
import json

from AppCore.nlpdatabase.terasus.terasus_item import MyItem
from AppCore.nlpdatabase.terasus.info.class_info import ClassInfo
from AppCore.nlpdatabase.terasus.info.property_info import PropertyInfo

class MyTerasus:
    def __init__(self, path):
        self.workpath = path
        self.terasus = dict()
        self.classes = dict()

    def __add_item(self, item):
        for i in item.words:
            if i in self.terasus.keys():
                self.terasus[i].append(item)
            else:
                self.terasus[i] = [item, ]

    def __load_classes(self):
        classpath = os.path.join(self.workpath, 'classes')
        for i in os.listdir(classpath):
            fpath = os.path.join(classpath, i)
            with open(fpath) as file:
                dt = json.load(file)
                item = MyItem(dt, 'class')
                self.__add_item(item)
                inf = ClassInfo(dt)
                self.classes[inf.system_name] = inf

    def __load_properties(self):
        classpath = os.path.join(self.workpath, 'properties')
        for i in os.listdir(classpath):
            fpath = os.path.join(classpath, i)
            with open(fpath) as file:
                dt = json.load(file)
                item = MyItem(dt, 'property')
                self.__add_item(item)
                inf = PropertyInfo(dt)
                self.classes[inf.system_name] = inf

    def load(self):
        self.__load_classes()
        self.__load_properties()
