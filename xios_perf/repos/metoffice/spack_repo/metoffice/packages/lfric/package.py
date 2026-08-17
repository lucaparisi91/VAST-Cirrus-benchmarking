# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess

from spack.package import *
from spack_repo.builtin.build_systems.generic import Package


class Lfric(Package):
    """Build the LFRic application from the Met Office build workflow."""

    homepage = "https://github.com/MetOffice/lfric_apps"
    git = "https://github.com/MetOffice/lfric_apps.git"
    
    version("3.2", branch="vn3.2")
    version("3.1.1", branch="vn3.1.1")

    resource(
        name="lfric_apps",
        placement="lfric_apps",
        git="https://github.com/MetOffice/lfric_apps.git",
        branch="vn3.1.1",
    )
    resource(
        name="lfric_core",
        placement="lfric_core",
        git="https://github.com/MetOffice/lfric_core.git",
        branch="vn3.1",
    )

    variant(
        "opt",
        values=("debug", "fast-debug", "production"),
        default="fast-debug",
        description="Optimization level passed to the LFRic build",
    )

    variant(
        "mesh_tools",
        default=False,
        description="Build the LFRic mesh tools",
    )
    
    depends_on("lfric-meta@3.2 + xios", type=("build","run") , when="@3.2")
    depends_on("lfric-meta@3.1.1 +xios", type=("build","run") , when="@3.1.1")
    depends_on("fcm", type="build")
    depends_on("python", type="build")
    depends_on("mpi", type="build")
    depends_on("c", type=("build", "link"))
    depends_on("fortran", type=("build", "link"))

    def install(self, spec, prefix):
        opt_level = self.spec.variants["opt"].value

        
        model = "gungho_model"

        root_dir = self.stage.source_path
        apps_dir = os.path.join(root_dir, "lfric_apps")
        core_dir = os.path.join(root_dir, "lfric_core")

        if not os.path.isdir(apps_dir):
            raise InstallError(f"Unable to locate the LFRic app checkout at {apps_dir}")

        if not os.path.isdir(core_dir):
            raise InstallError(f"Unable to locate the LFRic core checkout at {core_dir}")

        build_dir = os.path.join(apps_dir, "build")
        if not os.path.isdir(build_dir):
            raise InstallError(f"Unable to locate the LFRic build directory at {build_dir}")

        build_env = os.environ.copy()
        build_env["CRAY_ENVIRONMENT"] = "TRUE"
        build_env["PE_ENV"] = "GNU"
        build_env["FC"] = spec["mpi"].mpifc
        build_env["CC"] = spec["mpi"].mpicc
        build_env["CXX"] = spec["mpi"].mpicxx

        # Set the precision for the LFRic build to 32-bit
        build_env["RDEF_PRECISION"] = "32"
        build_env["R_TRAN_PRECISION"] = "32"
        build_env["R_BL_PRECISION"] = "32"
        build_env["R_SOLVER_PRECISION"] = "32"
        build_env["R_PHYS_PRECISION"] = "32"


        python_exe = which("python3") or which("python")
        if python_exe is None:
            raise InstallError("Unable to find a Python interpreter for the LFRic build")

        

        cmd = [
            "python",
            "local_build.py",
            "-p",
            "meto-azspice",
            "-v",
            "-c",
            core_dir,
            "-o",
            opt_level,
            model,
            "-j",
            str(make_jobs),
        ]

        subprocess.check_call(cmd, cwd=build_dir, env=build_env)

        install_tree(os.path.join(apps_dir, "applications", model, "bin"), prefix.bin)




        # Build the mesh tools if requested
        if "+mesh_tools" in self.spec:
            mesh_tools_dir = os.path.join(core_dir, "mesh_tools")
            if not os.path.isdir(mesh_tools_dir):
                raise InstallError(f"Unable to locate the LFRic mesh tools directory at {mesh_tools_dir}")
            cmd = [
                "make",
                "-j",
                str(make_jobs),
                "build"
            ]    
            
            subprocess.check_call(cmd, cwd=mesh_tools_dir, env=build_env)
            install_tree(os.path.join(mesh_tools_dir, "bin"), prefix.bin)

    def setup_run_environment(self, env):
        env.set("GUNGHO_MODEL_ROOT", self.prefix)
        env.prepend_path("PATH", self.prefix.bin)