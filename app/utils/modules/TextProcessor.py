from KeyProcessor import KeyProcessor
class TextProcessor(KeyProcessor):
    def __init__(self, name, data):
        # self.name = name
        # self.data = data
        super().__init__(name, data)

    def process(self, value):
        print(value)
        # self.process_key('return', value)
        if "value" in self.data:
            return self.data["value"].upper()
        # return self.data['value'].upper()