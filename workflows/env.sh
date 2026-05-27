source /work/z19/z19/lparisi/nfs-testing/workflows/cylc_env/bin/activate
export BENCHMARKS_ROOT=/work/z19/shared/lparisi/vast_lustre_benchmarks26
export HOME=${BENCHMARKS_ROOT}/runs
export CYLC_SITE_CONF_PATH=$(pwd)  # Point to the root of flow/global.cylc file.
export CYLC_VERSION=8
export PYTHONPATH=$(pwd)/lib/python:$PYTHONPATH