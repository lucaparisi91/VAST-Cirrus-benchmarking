import json
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt


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
    return data_long