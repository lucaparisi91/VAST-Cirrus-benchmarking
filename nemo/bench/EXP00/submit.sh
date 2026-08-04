#!/bin/bash
#SBATCH --nodes=13
#SBATCH --exclusive
#SBATCH --time=00:60:00
#SBATCH --ntasks-per-node=288
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

set -e 

module load PrgEnv-gnu
module load cray-hdf5-parallel
module load cray-netcdf-hdf5parallel

export PATH=/work/z19/z19/lparisi/nfs-testing/nemo/xios/xios3/bin:$PATH
module use /work/z19/z19/lparisi/nfs-testing/environments/benchmarks/modules/Core
module load hpctoolkit-gcc


export FI_CXI_RX_MATCH_MODE=hybrid
#export FI_CXI_OPTIMIZED_MRS=false
export FI_CXI_DEFAULT_CQ_SIZE=1048576
export SRUN_CPUS_PER_TASK=1

unset SLURM_NTASKS
unset SLURM_TASKS_PER_NODE
unset SLURM_NTASKS_PER_NODE
unset SLURM_NPROCS
module load xthi

#LAUNCHER="hpcrun -o hpctoolkit_nemo -t"
LAUNCHER=""

WORK_DIR=/work/z19/z19/lparisi/nfs-testing/nemo/bench/EXP00/run1
OUTPUT_DIR=/work/z19/z19/lparisi/nfs-testing/nemo/bench/EXP00/lustre
NEMO_DIR=/work/z19/z19/lparisi/nfs-testing/nemo/bench/nemo_5.0.2

module load darshan-runtime-gcc
mkdir -p $OUTPUT_DIR
export DARSHAN_LOG_DIR_PATH=$OUTPUT_DIR/darshan_logs
export DARSHAN_LOGPATH=$DARSHAN_LOG_DIR_PATH
export DARSHAN_CONFIG_PATH=$WORK_DIR/darshan.conf
mkdir -p $DARSHAN_LOG_DIR_PATH

# Move data from the example directory
mkdir -p $WORK_DIR
cd $WORK_DIR
rsync -rL $NEMO_DIR/cfgs/GYRE_PISCES/EXP00/* .
export PATH=$NEMO_DIR/cfgs/GYRE_PISCES/BLD/bin/:$PATH

mkdir -p $WORK_DIR/output

srun --mem=0 --het-group=0 --tasks=3000 --tasks-per-node=288 --cpus-per-task=1 --nodes=11 $LAUNCHER nemo.exe : --mem=0 --het-group=1 --tasks=16 --tasks-per-node=8 --nodes=2  --cpus-per-task=36  $LAUNCHER xios_server.exe

rm -r $WORK_DIR/output 
rm $WORK_DIR/*.nc

rsync -rL $WORK_DIR $OUTPUT_DIR