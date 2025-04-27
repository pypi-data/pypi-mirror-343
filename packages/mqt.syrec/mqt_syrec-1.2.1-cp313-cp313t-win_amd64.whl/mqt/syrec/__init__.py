# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""MQT SyReC library.

This file is part of the MQT SyReC library released under the MIT license.
See README.md or go to https://github.com/cda-tum/syrec for more information.
"""

from __future__ import annotations


# start delvewheel patch
def _delvewheel_patch_1_10_1():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'mqt_syrec.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_10_1()
del _delvewheel_patch_1_10_1
# end delvewheel patch

from ._version import version as __version__
from .pysyrec import (
    bitset,
    circuit,
    cost_aware_synthesis,
    gate,
    gate_type,
    line_aware_synthesis,
    program,
    properties,
    read_program_settings,
    simple_simulation,
)

__all__ = [
    "__version__",
    "bitset",
    "circuit",
    "cost_aware_synthesis",
    "gate",
    "gate_type",
    "line_aware_synthesis",
    "program",
    "properties",
    "read_program_settings",
    "simple_simulation",
]
