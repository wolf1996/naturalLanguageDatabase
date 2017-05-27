from AppCore.nlpdatabase.terasus.info.base_info import BaseInfo


class PropertyInfo(BaseInfo):
    def __init__(self, json_data):
        super(PropertyInfo, self).__init__(json_data)
        self.system_name = json_data["system_name"]
        self.range = json_data["range"]
        self.domain = json_data["domain"]
