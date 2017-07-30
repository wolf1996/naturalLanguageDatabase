class NodeContainer:
    def __init__(self, terasus, key_generator):
        self.id = None
        self.key_generator = key_generator
        self.is_a = []
        self.data_properties_resolved = dict()
        self.data_properties = []
        self.data_relations = []
        self.terasus = terasus

    def __create_base(self):
        bufkey = self.key_generator()
        res = "MATCH({}) - [: is_a * 0..]->({})\n".format(self.id, bufkey)
        res += "WHERE "
        res += '{}.system_name in '.format(bufkey)
        types = [i.system_name for i in self.is_a]
        res += str(types)
        res += '\n'
        return res

    def create_named_props(self):
        res = "MATCH ({}) WHERE ".format(self.id)
        buf = []
        for i in self.data_properties_resolved.items():
            buf.append("({}.{}=\'{}\')".format(self.id, i[0], i[1]))
        res += "AND".join(buf)
        return res

    def add_props(self, proper):
        prop = []
        rels = []
        for i in proper.is_a:
            prp = self.terasus.classes[i.system_name]
            if 'str' in prp.range:
                prop.append(prp)
            else:
                rels.append(prp)

        slist = []
        node = None
        for i in proper.range:
            if type(i) == str:
                slist.append(i)
            else:
                node = i
        relkey = self.key_generator()
        rg = self.key_generator()
        cypher = "MATCH ({}) -[{}*0..1]-> ({}) WHERE ".format(self.id, relkey, rg)
        proplst = []
        for i in prop:
            proplst.append("({}.{} in {})".format(self.id, i.system_name, str(slist)))
        if rels:
            proplst.append("(type({}[0]) in {})".format(relkey, str([i.system_name for i in rels])))
        cypher += "OR".join(proplst)
        cypher += "\n"
        if (node is not None) and rels:
            node.id = rg
            cypher += node.get_cypher()
        return cypher

    def create_relation(self, rel):
        relkey = self.key_generator()
        rg = self.key_generator()
        cypher = "MATCH ({}) -[{}]-> ({}) \n".format(self.id, relkey, rg)
        rel.id = relkey
        cypher += "WHERE "
        cypher += 'type({}) in '.format(relkey)
        types = [i.system_name for i in rel.is_a]
        cypher += str(types)
        cypher += '\n'
        dst = rel.range[0]
        dst.id = rg
        cypher += dst.get_cypher()
        return cypher

    def create_relationships(self):
        cyph = ''
        for i in self.data_relations:
            cyph += self.create_relation(i)
        return cyph

    def create_data_pops(self):
        cypher = ''
        for i in self.data_properties:
            cypher += self.add_props(i)
        return cypher

    def get_cypher(self):
        cypher = ''
        if self.is_a:
            cypher += self.__create_base()
        if self.data_properties_resolved:
            cypher += self.create_named_props()
        if self.data_relations:
            cypher += self.create_relationships()
        if self.data_properties:
            cypher += self.create_data_pops()
        return cypher
