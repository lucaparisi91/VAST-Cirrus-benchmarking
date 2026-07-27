import json
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import os


def load_reframe_report(filename) -> dict:
    """
    Load the ReFrame report from a JSON file.
    Args:
        filename (str): Path to the JSON file containing the ReFrame report.
    Returns:
        dict: Parsed JSON data from the report.
    """

    # Read the JSON file
    with open(filename, 'r') as file:
        data = json.load(file)
    return data



def get_performance_tables( data:dict) -> dict:
    """
    Extracts the performance table from the JSON data.

    Args:
        data (dict): The JSON data containing the reframe performance report.

    Returns:
        dict: A dictionary containing the test name to performance table mapping.
    """

    perf_tables={}

    for run in data["runs"]:
        for testcase in run["testcases"]:

            parameters=re.findall(r"%(\S+)=(\S+)", testcase["name"]) # Extract parameters from the test case name
            base_name=testcase["name"].split(r" ")[0] # Name of the test case ignoring parameters and variants
            
            testcase_perf={}
            testcase_perf["name"]=base_name

            for param_name, param_value in parameters:
                testcase_perf[param_name.split(".")[-1]]=param_value
            
            for perf_name, perf_value in testcase["perfvalues"].items():

                 perf_base_name=perf_name.split(r":")[-1] # Name of the performance metric ignoring variants
                 testcase_perf[perf_base_name]=perf_value[0]

            perf_table=pd.DataFrame([testcase_perf],index=[0])

            if base_name in perf_tables: # Do we already have data for this test case?
                perf_tables[base_name]=pd.concat([perf_tables[base_name], perf_table], ignore_index=True) # Concatenate the new performance table with the existing one for the same test case
            else:
                perf_tables[base_name]=perf_table # Add the test case to the perfermance tables dictionary
            
        return perf_tables

def post_process_cbenchio_table(data: pd.DataFrame) -> pd.DataFrame:
    """
    Post-processes the cbenchio performance table in a format amenable to plotting.

    Args:
        data (pd.DataFrame): The cbenchio performance table.
    """

    
    bandwidth_columns = [col for col in data.columns if col.startswith('bandwidth_')] # Identify the bandwidth columns
    id_columns = [col for col in data.columns if col not in bandwidth_columns] # All other columns identify the test
    data_long = data.melt(id_vars=id_columns, value_vars=bandwidth_columns,var_name="replica",value_name="bandwidth") #     # Pivot the bandwidth_x columns
    #sns.pointplot(data=data, x='nodes', y='bandwidth_0')
    data_long = data_long.drop("replica",axis=1)

     # Set defaults parameters 
    if "stripes" not in data_long.columns:
        data_long["stripes"] = "1"
    if "field_size_per_process_per_dimension" not in data_long.columns:
        data_long["field_size_per_process_per_dimension"] = "1048576"

    # Convert to MiB
    data_long["field_size_per_process_per_dimension"]=(data_long["field_size_per_process_per_dimension"].astype(int) )

    # Replace the number of stripes with the number of nodes when the number of stripes is set to "num_nodes"


    
    selection = data_long["stripes"] == "num_nodes"
    data_long.loc[selection, "stripes"] = data_long.loc[selection, "nodes"]


    data_long["nodes"] = data_long["nodes"].astype(int)
    data_long["tasks_per_node"] = data_long["tasks_per_node"].astype(int)
        
    data_long["stripes"] = data_long["stripes"].astype(int)
    data_long["filesystem"] = [get_file_system(base_path) for base_path in data_long["base_path"]]


    return data_long


def get_file_system(path: str) -> str:
    """Get the file system type for a given path.
    Args:
        path (str): The file path to check.

    Returns:
        str: The file system type ("VAST" or "LUSTRE").
    """
    
    if "vast" in path.split(os.sep):
        return "vast"
    else:
        return "lustre"

def load_cbenchio_reports(filenames):
    experiments=[]
    for filename in filenames:
        data= load_reframe_report(filename)
        tables=get_performance_tables(data)
        for test_case, table in tables.items():
            data = post_process_cbenchio_table(table)
            experiments.append(data)

           
    
    data=pd.concat(experiments).reset_index(drop=True).dropna()
    return data


def get_report_filenames(base_path, pattern="*.json", exclude_pattern=None):
    """Get a list of report filenames in the specified base path that match the given pattern and do not match the exclude pattern.
    Args:
        base_path (str): The base path to search for report files.
        pattern (str): The pattern to match report files (default: "*.json").
        exclude_pattern (str): The pattern to exclude report files (default: None).      
    Returns:
        list: A list of report filenames that match the given pattern and do not match the exclude pattern.         
    """
    report_filenames = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            for pat in [pattern] if isinstance(pattern, str) else pattern:
                if re.match(pat, file) and (exclude_pattern is None or not re.match(exclude_pattern, file)):
                    report_filenames.append(os.path.join(root, file))
    return report_filenames
