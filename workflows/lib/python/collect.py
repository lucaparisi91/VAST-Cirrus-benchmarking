from vernier import collect_vernier_data
import pandas as pd
import os
import sys
import parameters
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_performance_job(benchmark_folder: str, prefix: str="") -> pd.DataFrame:
    """
    Get the performance from the report.yaml file for a given job run.

    ::param benchmark_folder: The path of the benchmark folder 
    ::type benchmark_folder: str
    ::return: A pandas DataFrame with the performance results of the benchmark run.
    ::rtype: pd.DataFrame

    """

    benchmark_dirname = os.path.basename(benchmark_folder)

    # Read the report.yaml file
    report_file = os.path.join(benchmark_folder, "report.yaml")
    with open(report_file, 'r') as f:
        report = yaml.load(f, Loader=Loader)
    
    results= []
    for benchmark in report["benchmarks"]:
        for result in benchmark["results"]: # A row in the results table
            results_benchmark = parameters.get_parameters_from_label(benchmark_dirname[len(prefix):])
            
            results_benchmark["bandwidth"] = float(result["bandwidth"])
            results_benchmark["dataSize"] = float(result["dataSize"])/1e+9 * 2**30 # Convert from bytes to GiB
            
            results_benchmark["tasksPerNode"] = int(results_benchmark["tasksPerNode"])
            results.append(results_benchmark)

    
    return pd.DataFrame(results)


def get_performance(benchmarks_root: str, prefix: str="") -> pd.DataFrame:
    """
    Loop over all subfolders in the benchmarks root folder and get the performance results for each benchmark run.

    ::param benchmarks_root: The path of the benchmarks root folder 
    ::type benchmarks_root: str
    ::return: A pandas DataFrame with the performance results of all benchmark runs.
    ::rtype: pd.DataFrame

    """
    
    results = []
    for benchmark_folder in os.listdir(benchmarks_root):
        if benchmark_folder.startswith(prefix):
            performance = get_performance_job(os.path.join(benchmarks_root, benchmark_folder), prefix=prefix)
            results.append(performance)
    return pd.concat(results, ignore_index=True)