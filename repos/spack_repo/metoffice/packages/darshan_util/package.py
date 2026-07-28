from spack_repo.builtin.packages.darshan_util.package import DarshanUtil as DarshanUtilBase
from spack.package import *

class DarshanUtil(DarshanUtilBase):
    """
    Set the runtime environment for the darshan tool on EPCC systems.
    """
    maintainers("lucaparisi91")
    version("3.5.0", sha256="5299ae5407ef55f4503bfaa038cf8b01128d19238b10e3e20d980411c2e8b97c")
    url="https://github.com/darshan-hpc/darshan/releases/download/3.5.0/darshan-3.5.0.tar.gz"
