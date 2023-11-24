from KeyProcessor import KeyProcessor
class NumberProcessor(KeyProcessor):
    def __init__(self, name, data):
        # self.name = name
        # self.data = data
        super().__init__(name, data)

    def process(self, value):
        print(value)
        return self.data['value'] * 2