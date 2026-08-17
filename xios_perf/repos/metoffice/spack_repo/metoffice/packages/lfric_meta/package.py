# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from curses import version

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *

class LfricMeta(BundlePackage):
    """Dependencies of LFRic."""

    version("1.2")
    version("2.0")
    version("2.1")
    version("2.2")
    version("3.0")
    version("3.1.0")
    version("3.1.1")
    version("3.2")

    variant("xios", default=True, description="Whether to build with xios support")
    variant("vernier", default=False, description="Whether to build with vernier support",when="@1:2")
    variant("vernier", default=True, description="Whether to build with vernier support",when="@3:")
    

    # # Dependencies
    depends_on("mpi", type="run")
    depends_on("hdf5+mpi",type = "run")
    depends_on("netcdf-c+mpi", type="run")
    depends_on("netcdf-fortran", type="run")
    depends_on("yaxt", type="run")
    depends_on("py-jinja2", type="run")
    depends_on("py-psyclone@2.5.0", when='@:1.2', type="run")
    depends_on("py-psyclone@3.0.0", when='@2.0', type="run")
    depends_on("py-psyclone@3.1.0", when='@2.1:3.1.0', type="run")
    depends_on("py-psyclone@3.2.2", when='@3.1.1', type="run")
    depends_on("py-psyclone@3.3.1", when='@3.2', type="run")
    depends_on("py-pyyaml",when='@3.0:', type="run") 
    depends_on("rose-picker", type="run")


    depends_on("xios", type="run",when="+xios")
    depends_on("vernier", type="run",when="+vernier")
    depends_on("shumlib@13.0+openmp", type="run")
    depends_on("pfunit@4.12.0 +mpi +openmp", type="run")
    depends_on("fargparse", type="run")
    depends_on("gftl-shared", type="run")

    
    depends_on("cxx", type='build')
    depends_on("c", type='build')
    depends_on("fortran", type='build')


    # Set up environment paths
    def setup_run_environment(self, run_env):
        spec = self.spec

        # Compiler agnostic env vars
        run_env.set("FC", "ftn")
        run_env.set("LDMPI", "ftn")
        run_env.set("FPP", "cpp -traditional-cpp")
        
        if "vernier" in spec:
            run_env.set("USE_VERNIER", "true")
            run_env.set("USE_TIMING_WRAPPER", "true")

        else: # Use legacy timer if vernier is not enabled
            run_env.set("USE_LEGACY_TIMER", "true")
            run_env.set("USE_TIMING_WRAPPER", "true")


