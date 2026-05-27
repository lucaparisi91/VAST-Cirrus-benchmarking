from typing import List
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def expand_combinations(parameters: dict, repeats: int = 1) -> List[dict]:
    """
    Return a list of dictionaries. Each dictionary is a combination of the parameters provided in the parameters dictionary.
    
    :param parameters: Each key is a parameter name and each value is a list of possible values for that parameter. The function will return all possible combinations of these parameters.
    :type parameters: dict
    :param repeats: The number of times to repeat each combination.
    :type repeats: int
    :return: A list of dictionaries, where each dictionary is a combination of the parameters provided in the parameters dictionary.
    :rtype: List[dict]
    """
    
    combinations = [{"repeatIndex": i} for i in range(repeats)]
    
    for key, values in parameters.items():
        new_combinations = []
        for value in values:
            for combination in combinations:
                new_combination = combination.copy()
                new_combination.update({key: value})
                new_combinations.append(new_combination)
        combinations = new_combinations.copy()
    
    return combinations

def get_label(parameters: dict):
    """
    Get a label for a combination of parameters. The label is a string that concatenates the parameter names and values in the format "key_value".
    
    :param parameters: A dictionary where each key is a parameter name and each value is the value of that parameter for this combination.
    :type parameters: dict
    :return: A string label for the combination of parameters.
    :rtype: str
    """

    label = ""

    for key, value in parameters.items():
        label += f"{key}_{value}_"

    return label[:-1]

def get_parameters_from_label(label: str) -> dict:
    """
    Get a dictionary of parameters from a label. The label is a string that concatenates the parameter names and values in the format "key_value".
    
    :param label: A string label representing the combination of parameters.
    :type label: str
    :return: A dictionary where each key is a parameter name and each value is the value of that parameter for this combination.
    :rtype: dict
    """

    parameters = {}
    key_values = label.split("_") # Generates a list of alternating keys and values, e.g. ["key1", "value1", "key2", "value2", ...]

    for key, value in zip(key_values[::2], key_values[1::2]):
        parameters[key] = value
    
    return parameters

def from_yaml(file_path: str) -> dict:
    """
    Load parameters from a YAML file.
    
    :param file_path: The path to the YAML file containing the parameters.
    :type file_path: str
    :return: A dictionary of parameters loaded from the YAML file.
    :rtype: dict
    """
    
    with open(file_path, "r") as f:
        parameters = yaml.load(f, Loader=Loader)
    
    return parameters