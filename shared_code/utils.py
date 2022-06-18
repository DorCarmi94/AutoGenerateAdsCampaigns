import yaml

def load_yaml(document):
    with open(document, 'r') as stream:
        return yaml.safe_load(stream)