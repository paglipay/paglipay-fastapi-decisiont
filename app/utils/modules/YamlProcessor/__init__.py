from KeyProcessor import KeyProcessor
import yaml
class YamlProcessor(KeyProcessor):
    def __init__(self, name, data):
        # self.name = name
        # self.data = data
        super().__init__(name, data)

    def process(self, value):
        print('YAML PROCESSOR HERE')
        print(value)
        print(self.data)
        if "save_as" in value["data"]:
            print('SAVE AS HERE')
            print(value["data"]["save_as"])
            with open(value["data"]["save_as"], 'w') as outfile:
                yaml.dump(self.data["value"], outfile, default_flow_style=False)

        return yaml.dump(self.data["value"], default_flow_style=False)
        # self.process_key('return', value)
        # return self.data['value'].upper()