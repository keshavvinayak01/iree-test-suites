# Copyright 2024 The IREE Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import pytest
from compile_run import CompilationUnitRunItem
from pathlib import Path
import os
import logging
from dataclasses import dataclass
import json

THIS_DIR = Path(__file__).parent
logger = logging.getLogger(__name__)
DEVICE = os.getenv("DEVICE", default="local")


def pytest_addoption(parser):
    parser.addoption(
        "--test-file-directory",
        action="store",
        help="The directory of quality test JSON files to build and run test cases",
    )


def pytest_sessionstart(session):
    logger.info("Pytest compilation test session is starting")

    # Collect all .json files for compilation tests.
    files: list[Path] = []
    test_file_directory = Path(session.config.getoption("test_file_directory"))
    test_files = sorted(test_file_directory.glob("**/*.json"))
    for test_file in test_files:
        with open(test_file, "r") as file:
            test_config = json.load(file)
        assert "device" in test_config
        if test_config["device"] == DEVICE:
            files.append(test_file)
    session.config.test_files = files


class SharkTankCompilationUnitTests(pytest.File):
    def collect(self):
        for file_path in self.session.config.test_files:
            yield CompilationUnitRunItem.from_parent(
                self, file_path=file_path, name=file_path.stem
            )


def pytest_collect_file(parent, file_path):
    if "compile_run" in str(file_path):
        return SharkTankCompilationUnitTests.from_parent(parent, path=file_path)
