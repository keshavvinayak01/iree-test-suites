# Copyright 2025 The IREE Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import pytest
from ireers_tools import *
import os
from pathlib import Path
import json

THIS_DIR = Path(__file__).parent
# compiled files will live in the previous directory, so quality/benchmark
# tests can access those and no need to recompile
PARENT_DIR = Path(__file__).parent.parent
ARTIFACT_DIR = os.getenv("TEST_OUTPUT_ARTIFACTS", default=str(PARENT_DIR))
# TODO: This should just be chip, instead of ROCM_CHIP.
CHIP = os.getenv("ROCM_CHIP", default="gfx942")
SKU = os.getenv("SKU", default="mi300")


class CompilationUnitRunItem(pytest.Item):
    def __init__(self, file_path: Path, **kwargs):
        super().__init__(**kwargs)
        self.file_path: Path = file_path
        self.unit_name: str = self.file_path.stem
        self.vmfb_dir = Path(ARTIFACT_DIR) / self.unit_name

        with open(self.file_path, "r") as file:
            # Parse the JSON spec.
            data = json.load(file)
            # mlir: required
            mlir_path = data.get("mlir")
            assert mlir_path
            self.mlir = fetch_source_fixture(
                data.get("mlir"), group=self.unit_name, name=(self.unit_name + ".mlir")
            )
            # device: required
            self.device = data.get("device")
            assert self.device
            # compiler_flags: optional
            self.compiler_flags: list[str] = data.get("compiler_flags", [])
            # xfail: optional
            xfail = data.get("xfail", {})
            self.xfail: str = xfail.get(SKU, None)
            # tuner_file: optional
            tuner_file = data.get("tuner_file", {})
            self.tuner_file: str | None = tuner_file.get(SKU, None)

    def _build_compile_flags(self) -> list[str]:
        compiler_flags = self.compiler_flags
        compiler_flags += [f"--iree-hal-target-device={self.device}"]
        # Set target features.
        # TODO: Plumb these flags as a "device configuration" json on the
        # project (iree / iree plugin) side, to not hardcode for a single
        # device.
        if self.device == "hip":
            compiler_flags += [f"--iree-hip-target={CHIP}"]
        # Create fake weights as a backup, in case the user does not have real
        # weights for benchmarking.
        fake_weights = Artifact(group=self.unit_name, name="fake_weights.irpa")
        compiler_flags += [f"--iree-opt-splat-parameters={fake_weights.path}"]
        # TODO: tuner_file.
        return compiler_flags

    def runtest(self):
        try:
            compiler_flags = self._build_compile_flags()
            vmfb_path = (self.vmfb_dir / self.unit_name).with_suffix(".module.vmfb")
            iree_compile(self.mlir, compiler_flags, vmfb_path)
        except Exception as e:
            if self.xfail is not None:
                pytest.xfail(self.xfail)
            raise e

        if self.xfail is not None:
            pytest.fail(f"Test was expected to xfail with reason: {self.xfail}")
