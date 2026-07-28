# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *

class RosePicker(PythonPackage):

    """rose_picker - utility for LFRIC."""

    git = "https://github.com/MetOffice/rose_picker.git"

    version("2.0.0", branch="main")

    extends("python@3:")

    depends_on("subversion", type="build")
    depends_on("py-setuptools", type="build")

    
    # def install(self, spec, prefix):
    #     install_tree(src=".", dest=prefix, symlinks=True, ignore=None)
    
    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self.spec.prefix.lib.python)
