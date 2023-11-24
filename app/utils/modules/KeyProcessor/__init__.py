import pprint as pp
import json
import yaml

class KeyProcessor:
    def __init__(self, name, data={}):
        self.processor_name = name
        self.data = data
        self.data.update({self.processor_name: []})
        self.processing_result_var = False

    def process_key(self, config_string, value):
        config_boolean = False

        # Define the actions for each config string
        switch_case = {
            'True': lambda: True,
            'False': lambda: False,
            'return': lambda: self.processing_result(value),
            'jobs': lambda: self.process_jobs(value),
            'processors': lambda: self.process_processors(value)
        }

        # Check if the config string is in the switch case dictionary
        if config_string in switch_case:
            config_boolean = switch_case[config_string]()
        
        return config_boolean

    def processing_result(self, value):
        # Process the result value
        print('Processing result: ', value)
        if value == 'True':
            self.processing_result_var = True
        elif value == 'False':
            self.processing_result_var = False
        else:
            self.processing_result_var = value
        return self.processing_result_var

    def process_jobs(self, value):
        # Process the jobs value
        from DecisionTree import DecisionTree
        print('DecisionTree HERE:', value)
        decisionTree = DecisionTree(value, data=self.data)

    def process_processors(self, value):
        # Process the processors value
        if ".json" in value:
            if value in self.data:
                value = self.data[value]
            else:
                with open(value) as f:
                    value = json.load(f)
        for processor in value:
            if "enable" in processor and not processor["enable"]:
                continue
            module_name = processor['name']
            data = self.process_configuration(processor['data'])
            my_class = getattr(__import__(module_name), module_name)
            myClass = my_class(module_name, data)
            if module_name not in self.data:
                self.data[module_name] = []
            if 'return' in processor and not processor['return']:
                pass
            else:
                self.data[module_name].append(myClass.process(processor))

    def process_configuration(self, configuration):
        # Process the configuration
        if isinstance(configuration, list):
            for item in configuration:
                self.process_configuration(item)
                    
        elif isinstance(configuration, dict):
            print('Processing dict: ', configuration)
            if "open" in configuration:
                file_path = configuration["open"]
                if '.json' in file_path:
                    with open(file_path) as f:
                        return json.load(f)
                elif '.txt' in file_path:
                    with open(file_path) as f:
                        return f.read()
                elif '.yml' in file_path:
                    with open(file_path, 'r') as yaml_file:
                        data = yaml.safe_load(yaml_file)
                    return data
            else:
                return configuration

        else:
            return configuration

    def process_value(self, value):
        # Process the value
        print('Processing value: ', value)
        self.data[self.processor_name].append(value)
        return True
    
    def process(self, value):
        # Process the value
        print('Processing process value: ')
        pp.pprint(value)
        return value

    def process_configuration(self, configuration):
        # Process the configuration
        if isinstance(configuration, list):
            for item in configuration:
                self.process_configuration(item)
                    
        elif isinstance(configuration, dict):
            print('Processing dict: ', configuration)
            if "open" in configuration:
                if '.json' in configuration["open"]:
                    with open(configuration["open"]) as f:
                        return json.load(f)
                elif '.txt' in configuration["open"]:
                    with open(configuration["open"]) as f:
                        return f.read()
                elif '.yml' in configuration["open"]:
                    with open(configuration["open"], 'r') as yaml_file:
                        data = yaml.safe_load(yaml_file)
                    return data
            else:
                return configuration

        else:
            return configuration