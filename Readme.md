# VAST benchmarking

This repo contains scripts and results from benchmarking VASP.
The cylc framework is used to run the benchmarks. Some paths are hardcoded and you will need to change them.
- The workflows directory contains the script to reproduce the benchmarks
- The anal directory contains jupyter notebooks for producing plots from the data
- The results directory contains processed results from the benchmarks

## Tools used

- cbenchio ( https://github.com/lucaparisi91/cbenchio )


## Running the benchmarks ( reframe )

Reframe was used to run cbenchio benchmarks 

- Branch used: https://github.com/lucaparisi91/epcc-reframe/tree/cbenchio2
- Launch script: [run-reframe/reframe.sh](run-reframe/reframe.sh)

## Running the benchmarks ( workflows)
These are deprecated tests, run before the software upgrade
Go into the workflows directory and create a python environment

```bash
module load cray-python
python3 -m venv cylc_env
source cylc_env/bin/activate
pip install -r requirements.txt
```

Once you have created an environment you can run the benchmark using

```bash
cylc vip -n <my_benchmark_name> -S benchmark_config='"<my_yaml_config>"'
```