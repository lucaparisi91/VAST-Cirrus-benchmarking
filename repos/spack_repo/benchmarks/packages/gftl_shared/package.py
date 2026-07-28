# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

from spack_repo.builtin.packages.gftl_shared.package import GftlShared as BuiltinGftlShared


class GftlShared(BuiltinGftlShared):

  @property
  def home(self):
    return Prefix(f"{self.spec.prefix}/GFTL_SHARED-{self.version.up_to(2)}")

  def setup_run_environment(self, env):
    """Setup custom variables in the generated module file"""
    env.prepend_path("FFLAGS", "-I" + self.home.include, " ")
    env.prepend_path("LDFLAGS", "-L" + self.home.lib, " ")