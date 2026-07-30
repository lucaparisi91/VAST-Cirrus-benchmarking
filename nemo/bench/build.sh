#git clone --branch 5.0.2 https://forge.nemo-ocean.eu/nemo/nemo.git nemo_5.0.2

module use /mnt/lustre/e1000/home/z19/z19/lparisi/nfs-testing/environments/benchmarks/modules/Core
module load PrgEnv-gnu
module load cray-hdf5-parallel
module load cray-netcdf-hdf5parallel

CLEAN=1

XIOS_ROOT=/work/z19/z19/lparisi/nfs-testing/nemo/xios/xios3
export PATH=$XIOS_ROOT/bin:$PATH
export CPATH="$XIOS_ROOT/inc:$CPATH"
export LIBRARY_PATH="$XIOS_ROOT/lib:$LIBRARY_PATH"
export FFLAGS="-I$XIOS_ROOT/inc $FFLAGS"
export LDFLAGS="-L$XIOS_ROOT/lib -lxios -lstdc++ -I$XIOS_ROOT/inc -Wl,-rpath=$XIOS_ROOT/lib  $LDFLAGS"
NEMO_DIR=$(pwd)/nemo_5.0.2
cd $NEMO_DIR

export CC=cc
export CXX=CC
export FC=ftn

if [ $CLEAN -eq 1 ]; then
    ./makenemo -r GYRE_PISCES --clean 
fi

./makenemo -r GYRE_PISCES  -m archer2-gnu -j 16 2>&1 | tee build_nemo.log