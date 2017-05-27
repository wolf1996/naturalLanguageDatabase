
class OntologyLoader:
    def __init__(self, ontology, neo):
        self.ontology = ontology
        self.neo = neo
        self.ontology.sync_reasoner()
        self.nodes = dict()
        self.properties = dict()

    def add_class(self, elem_to_add):
        node = self.neo.node(system_name=elem_to_add.name)
        self.nodes[elem_to_add] = node
        pass

    def resolve(self, prop, src, dst):
        propname = prop.name
        n1 = self.nodes[src]
        n2 = self.nodes[dst]
        rel = n1.relationships.create(propname, n2)
        self.properties[prop] = rel
        return rel

    def add_abstract_property(self, elem_to_add):
        if not set(elem_to_add.range).issubset(set(self.ontology.classes)):
            self.properties[elem_to_add] = None
            return
        lst = [(i, j) for i in elem_to_add.domain for j in elem_to_add.range]
        for i in lst:
            self.resolve(elem_to_add, *i)
        pass

    def add_instance(self, elem_to_add):
        node = self.neo.node(system_name=elem_to_add.name)
        self.nodes[elem_to_add] = node
        pass

    def apply_prop(self, owlnode, prop):
        if self.properties[prop] is None:
            attr_val = getattr(owlnode, prop.name)
            if attr_val:
                self.nodes[owlnode][prop.name] = attr_val
        else:
            for i in getattr(owlnode, prop.name):
                self.nodes[owlnode].relationships.create(prop.name, self.nodes[i])

    def recursive_apply(self, cls, prop):
        for i in cls.__subclasses__():
            print(i)
            if i in self.nodes:
                if hasattr(self.nodes[i], prop.name):
                    self.apply_prop(i, prop)

        for i in cls.instances():
            if hasattr(self.nodes[i], prop.name):
                self.apply_prop(i, prop)

    def add_relation(self, rel):
        for i in rel.domain:
            self.recursive_apply(i, rel)
            pass

    def add_relationships(self):
        for i in self.properties.keys():
            self.add_relation(i)

    def add_include(self, base, included):
        bclass = self.nodes[base]
        iclass = self.nodes[included]
        bclass.relationships.create("include", iclass)
        iclass.relationships.create("is_a", bclass)

    def add_includes(self):
        for i in self.ontology.classes:
            for j in i.is_a:
                if j in self.ontology.classes:
                    self.add_include(j, i)
        for i in self.ontology.instances:
            for j in i.is_a:
                if j in self.ontology.classes:
                    self.add_include(j, i)
        pass

    def load_classes(self):
        for i in self.ontology.classes:
            self.add_class(i)
        for i in self.ontology.instances:
            self.add_instance(i)
        for i in self.ontology.properties:
            self.add_abstract_property(i)
        self.add_relationships()
        self.add_includes()
