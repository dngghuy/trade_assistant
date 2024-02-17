import yaml


def read_yml_config(path):
    with open(path, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    return data