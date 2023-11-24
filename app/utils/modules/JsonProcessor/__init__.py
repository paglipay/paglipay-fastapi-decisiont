from KeyProcessor import KeyProcessor
import json
class JsonProcessor(KeyProcessor):
    def __init__(self, name, data):
        # self.name = name
        # self.data = data
        super().__init__(name, data)

    def process(self, value):
        print('JSON PROCESSOR HERE')
        print(value)
        print(self.data)
        if "save_as" in value["data"]:
            print('SAVE AS HERE')
            print(value["data"]["save_as"])
            # Save as json
            with open(value["data"]["save_as"], 'w') as outfile:
                json.dump(self.data["value"], outfile, indent=4)

        return self.data["value"]
        # self.process_key('return', value)
        # return self.data['value'].upper()