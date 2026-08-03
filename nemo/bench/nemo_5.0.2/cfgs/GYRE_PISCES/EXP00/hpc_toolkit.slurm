#!/bin/bash
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=00:20:00
#SBATCH --ntasks-per-node=288
#SBATCH --partition=standard
#SBATCH --qos=short
#SBATCH --distribution=block:block
#SBATCH --cpus-per-task=1
#SBATCH --hint=nomultithread    
#SBATCH --export=all

module load PrgEnv-gnu
module load cray-python

module use /work/z19/z19/lparisi/nfs-testing/environments/benchmarks/modules/Core
module load hpctoolkit-gcc


date
hpcstruct hpctoolkit_nemo/
date
hpcprof hpctoolkit_nemo/
date