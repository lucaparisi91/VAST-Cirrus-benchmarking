set -e

module load cray-python
module load reframe/4.8.4
REFRAME_ROOT=/work/z19/z19/lparisi/nfs-testing/epcc-reframe # Root directory of the repository
TESTS_ROOT=$REFRAME_ROOT/tests/
source /work/z19/z19/lparisi/nfs-testing/cbenchio/run/cbenchio_env/bin/activate
# -J qos=reservation -J reservation=2026-06-kernel -J partition=maintenance-standard-only

#cs-n[0432-0435]


module use /mnt/lustre/e1000/home/z19/z19/lparisi/nfs-testing/environments/benchmarks/modules/Core

reframe -R -C $REFRAME_ROOT/configuration/cirrus-ex.py --keep-stage-files -c $TESTS_ROOT -J qos=reservation -J reservation=VAST -J partition=maintenance-standard  -J exclusive -J time=00:40:00 -n cbenchio_posix_sequential -r --report-file performance.json  --performance-report 2>&1 | tee run_tests.log # Run the regression tests with ReFrame, using the benchio executable specified by the -S option on the Cirrus-ex platform.
