set -e 
set -x

OPT="dev"
COMPILER="GNU"
DOWNLOAD=1
BRANCH="xios-3.0.4.0" # main
CLEAN=0
CRAYPAT=0 # Set to 1 to enable CrayPat performance analysis tools
XIOS="xios3" # XIOS version to build with. Allowed values are xios2 and xios3


# load compiler specific modules
set +x # Disable command echoing to limit noise 
if [ "$COMPILER" = "GNU" ]; then
    module load PrgEnv-gnu
fi

if [ $CRAYPAT -eq 1 ]; then
    module load perftools
fi

module load cray-hdf5-parallel
module load cray-netcdf-hdf5parallel/4.9.0.17
set -x # Re-enable command echoing after loading modules


XIOS_DIR=$XIOS
# Clone XIOS repository if DOWNLOAD is set
if [ $DOWNLOAD -eq 1 ];
then
    git clone -b $BRANCH https://gitlab.in2p3.fr/ipsl/projets/xios-projects/xios.git $XIOS_DIR
    # Set architecture dependent configuration files
    cp -r arch/* $XIOS_DIR/arch/
fi



# Build XIOS
cd $XIOS_DIR

if [ $CLEAN -eq 1 ];
then
    # Clean previous builds
    rm -rf ./obj 
    rm -rf ./bin
    rm -rf ./lib
fi

./make_xios --$OPT --arch GCC_CRAY_EX4000 --job 16

if [ $CRAYPAT -eq 1 ];
then
    mkdir -p tmp
    cp obj/*.o tmp
    cp lib/*.a tmp
    cd lib
    ln -s libxios.a lib__fcm__xios_server.a
    cd ../bin
    rm -f xios_server.exe+pat 
    rm -f xios_server.exe+pat+mpi
    pat_build xios_server.exe
    pat_build -g mpi -o xios_server.exe+pat+mpi xios_server.exe
fi