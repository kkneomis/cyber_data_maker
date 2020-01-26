import json

def load_json_config(config_path):
    """Open a json file and return the contents in json format"""
    try:
        with open(config_path, 'r') as f:
            return dotdict(json.load(f))
    except IOError:
        print("Could not load config: Invalid config path")
    except Exception as e:
        print("Could not load config", e)


class dotdict(dict):
    """
    dot.notation access to dictionary attributes
    thanks to: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
    