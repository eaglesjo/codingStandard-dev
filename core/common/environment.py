from __future__ import annotations

"""Shared runtime environment profiler for all codingStandard domains."""

import json
import os
import platform
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

STANDARD_VERSION = "2.0.0"


@dataclass(frozen=True)
class EnvironmentProfile:
    standard_version: str
    os: str
    architecture: str
    python: str
    executable: str
    ide: str
    execution_environment: str
    execution_type: str
    jupyter: bool
    colab: bool
    cpu_count: int | None
    ram_total_gb: float | None
    ram_available_gb: float | None
    disk_total_gb: float | None
    disk_free_gb: float | None
    accelerator_vendor: str | None
    accelerator_name: str | None
    vram_total_gb: float | None
    vram_free_gb: float | None
    cuda_available: bool
    cuda_version: str | None
    rocm_available: bool
