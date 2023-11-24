import json, yaml
import sys

class DecisionTree:
    def __init__(self, configuration, tree_name='', module_instances={}, current_module_name=None, data={}):
        self.tree_name = tree_name
        self.configuration = configuration
        self.module_instances = module_instances
        self.current_module_name = current_module_name
        self.data = data
        self.processing_result = False
        sys.path.append('./modules')
        self.start_processing(self.configuration)

    def initialize_module(self, module_name):
        if module_name in self.module_instances:
            self.current_module_name = module_name
        else:
            module_class = getattr(__import__(module_name), module_name)
            self.current_module_name = module_name
            self.module_instances[self.current_module_name] = module_class(module_name, self.data)

    def start_processing(self, configuration):
        self.process_configuration(configuration)

    def process_key_value(self, key, value):
        if '.json' in key:
            if value in self.data:
                decision_tree = DecisionTree(self.data[key], key, self.module_instances, self.current_module_name, self.data)
            else:
                decision_tree = DecisionTree(json.load(open(key)), key, self.module_instances, self.current_module_name, self.data)
            decision_tree_processing_result = decision_tree.processing_result
            print('Decision tree processing result: ', decision_tree_processing_result)
            return decision_tree_processing_result
        
        else:
            return_val = self.module_instances[self.current_module_name].process_key(key, value)
            if 'processing_result' in self.module_instances[self.current_module_name].__dict__:
                self.processing_result = self.module_instances[self.current_module_name].processing_result
            return return_val

    def process_value(self, value):
        if '.json' in value:
            if value in self.data:
                decision_tree = DecisionTree(self.data[value], value, self.module_instances, self.current_module_name, self.data)
            else:
                decision_tree = DecisionTree(json.load(open(value)), value, self.module_instances, self.current_module_name, self.data)
            return decision_tree.processing_result
        
        if '.yml' in value:
            if value in self.data:
                data = yaml.safe_load(self.data[value])
                decision_tree = DecisionTree(data, value, self.module_instances, self.current_module_name, self.data)
            else:                
                with open(value, 'r') as yaml_file:
                    data = yaml.safe_load(yaml_file)
                    print('YML data: ', data)
                decision_tree = DecisionTree(data, value, self.module_instances, self.current_module_name, self.data)
            return decision_tree.processing_result
        else:
            return self.module_instances[self.current_module_name].process_value(value)

    def process_configuration(self, configuration):
        if isinstance(configuration, list):
            for item in configuration:
                # if self.process_configuration(item) == False:
                #     pass
                self.process_configuration(item)
                    
        elif isinstance(configuration, dict):
            for key, value in configuration.items():
                if key == 'import':
                    self.initialize_module(value)
                else:                        
                    if self.process_key_value(key, value):
                        return self.process_configuration(value)
        else:
            return self.process_value(configuration)