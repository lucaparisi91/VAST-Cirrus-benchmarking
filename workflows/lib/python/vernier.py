import pandas as pd
from parameters import get_parameters_from_label
import os

def to_df(vernier_file: str)   -> pd.DataFrame:
    """Reads a vernier output file and converts it to a pandas DataFrame.
        
    ::param vernier_file: The path to the vernier output file.
    ::returns: A pandas DataFrame containing the data from the vernier output file.
    """

    data=pd.read_csv(vernier_file,delimiter='\s+',header=5,names=["Time","Cumul","Self","Total","Calls","Self.per.call","Total.per.call","Routine"])
    return data

def collect_vernier_data( folder: str) -> pd.DataFrame:
    """Collects vernier data from a lfric_atm working directory and returns it as a pandas DataFrame.
    
    ::param folder: The path to the folder containing the vernier output files.
    ::returns: A pandas DataFrame containing the collected vernier data, annotated with the parameters extracted from the folder name.
    """
    
    vernier_file = f"{folder}/vernier-output-lfric_atm-0" # Output file predicted by Vernier

    data = to_df(vernier_file)
    folder_name = os.path.split(folder)[-1]
    
    # Extract parameters from the folder name, assuming a convenction for the folder name
    app="lfric_atm"
    label=folder_name[len(app + "_"):]
    parameters=get_parameters_from_label(label)
    for key, value in parameters.items():
        data[key] = value
    return data