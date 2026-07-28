# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *

class Cbenchio(CMakePackage):
    """Cbenchio is a benchmarking tool for I/O performance."""

    #homepage = "https://www.cp2k.org"
    url = "https://github.com/lucaparisi91/cbenchio/archive/refs/tags/v0.1.0.tar.gz"
    git = "https://github.com/lucaparisi91/cbenchio"
    #list_url = "https://github.com/cp2k/cp2k/releases"

    maintainers("lucaparisi91")
    
    version("master", branch="master")
    
    variant("logger_level",default="INFO", description="Logger level", values=("DEBUG","INFO","WARNING","NONE"))
    
    depends_on("mpi",type=("build","link"))
    
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("hdf5+mpi", type=("build","link"))
    depends_on("netcdf-c+mpi", type=("build","link"))
    

    root_cmakelists_dir = "cbenchio"

    def cmake_args(self):
        return [self.define_from_variant("LOGGER_LEVEL", "logger_level"),
]
    
    
   


