#!/bin/bash
#SBATCH --nodes=12
#SBATCH --exclusive
#SBATCH --time=00:20:00
#SBATCH --ntasks-per-node=200
#SBATCH --partition=standard
#SBATCH --qos=short
#SBATCH --distribution=block:block
#SBATCH --cpus-per-task=1
#SBATCH --hint=nomultithread    
#SBATCH --export=all
#SBATCH --qos=reservation
#SBATCH --reservation=VAST
#SBATCH --partition=standard
#SBATCH --exclusive

module load PrgEnv-gnu
module load cray-hdf5-parallel
module load cray-netcdf-hdf5parallel

export PATH=/work/z19/z19/lparisi/nfs-testing/nemo/xios/xios3/bin:$PATH

export FI_CXI_RX_MATCH_MODE=hybrid
#export FI_CXI_OPTIMIZED_MRS=false
export FI_CXI_DEFAULT_CQ_SIZE=1048576
export SRUN_CPUS_PER_TASK=1

unset SLURM_NTASKS
unset SLURM_TASKS_PER_NODE
unset SLURM_TASKS_PER_NODE
unset SLURM_NPROCS

srun --mem=0 --nodes=10 --cpus-per-task=1 --ntasks=288   --hint=nomultithread  --distribution=block:block ./nemo 
 : --mem=0 --nodes=2 --ntasks=48 --cpus-per-task=12 --ntasks-per-node=24 --distribution=block:block --hint=nomultithread $LAUNCHER xios_server.exe