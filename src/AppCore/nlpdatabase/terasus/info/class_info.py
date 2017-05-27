from AppCore.nlpdatabase.terasus.info.base_info import BaseInfo


class ClassInfo(BaseInfo):
    def __init__(self, json_data):
        super(ClassInfo, self).__init__(json_data)
        self.system_name = json_data["system_name"]