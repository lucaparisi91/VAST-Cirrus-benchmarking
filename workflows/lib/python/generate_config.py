
import yaml
import argparse
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def generate_posix_config( parameters: dict, filename: str) -> None:

    """
    Generate a configuration file for the POSIX benchmark based on the provided parameters.
    
    :param parameters: A dictionary where each key is a parameter name and each value is the value of that parameter for this combination.
    :type parameters: dict
    :param filename: The name of the file where the configuration will be saved.
    :type filename: str
    :return: None
    :rtype: None
    """

    template={
        "name": "write",
        "API": "posix",
        "filePerProcess": True,
        "processorGrid": [0,0,0],
        "shape": [2147483648,1,1],
        "paths": ["data"],
        "repeat": 20,
        "sync": True,
        "operation": "write",
        "chunkSize": 4194304,
        "content": "random",
        "direct": False,
        "alignment": 4096,
        "fields": 1
    }
    
    size_of_dtype = 8 # (Bytes) Assuming we are writing 64-bit floating point numbers.

    n_elements = int(parameters["chunkSize"] * parameters["chunksPerTask"] * 2**20/ size_of_dtype ) # Total number of elements to write per process. chunkSize is in MiB.
    
    if (parameters["singleFile"] ):
        n_elements = n_elements * parameters["tasksPerNode"] * parameters["nodes"] # If all processes write to the same file, we need to multiply by the total number of processes to get the total number of elements to write per process.
    
    template["shape"] = [n_elements, 1, 1]
    
    # File per process or all processes write to the same file ?
    if (parameters["singleFile"]):
        template["filePerProcess"] = False
    else:
        template["filePerProcess"] = True

    template["paths"]=[parameters["path"] ]
    template["repeat"] = parameters["repeat"]

    # Write the configuration to a yaml file
    with open(filename, 'w') as file:
        yaml.dump( {
            "benchmarks" : [template]
        }, file, Dumper=Dumper)
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate POSIX benchmark configuration.")
    parser.add_argument("--nodes", type=int, default=1, help="Number of nodes")
    parser.add_argument("--tasksPerNode", type=int, default=1, help="Number of tasks per node")
    parser.add_argument("--chunkSize", type=int, default=4, help="Chunk size in MiB")
    parser.add_argument("--chunksPerTask", type=int, default=32, help="Number of chunks per task")
    parser.add_argument("--direct", action='store_true', help="Use direct I/O")
    parser.add_argument("--path", type=str, default="data", help="Path to write the data")
    parser.add_argument("--singleFile", action='store_true', help="Use single file for all processes")
    parser.add_argument("--repeat", type=int, default=1, help="Number of times to repeat each experiment")
    parser.add_argument("--output", type=str, default="config.yaml", help="Output file name")

    args= parser.parse_args()
    parameters = {
        "nodes" : args.nodes,
        "tasksPerNode" : args.tasksPerNode,
        "chunkSize" : args.chunkSize, # (MiB)
        "chunksPerTask" : args.chunksPerTask, 
        "direct" : args.direct, # User direct I/O ?
        "path" : args.path,
        "singleFile" : args.singleFile,
        "repeat" : args.repeat
        
    }

    generate_posix_config(parameters, args.output)
