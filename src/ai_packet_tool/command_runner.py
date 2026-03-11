"""Command execution utilities for the AI packet workflow tool."""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class WorkflowStep:
    """Single executable workflow step definition."""

    name: str
    command: str


class WorkflowExecutionError(RuntimeError):
    """Raised when a workflow step exits with non-zero code."""


def run_steps(
    steps: Sequence[WorkflowStep],
    interval_seconds: int,
    workdir: Path,
    dry_run: bool = False,
) -> None:
    """Run workflow steps sequentially with a fixed interval between each step.

    Args:
        steps: Ordered workflow step list.
        interval_seconds: Seconds to wait between steps.
        workdir: Working directory where commands are executed.
        dry_run: If True, print commands only without executing.

    Raises:
        WorkflowExecutionError: If any step execution fails.
    """

    if interval_seconds < 0:
        raise ValueError("interval_seconds must be >= 0")

    _ensure_directory(workdir)

    for index, step in enumerate(steps, start=1):
        print(f"[{index}/{len(steps)}] {step.name}")
        print(f"$ {step.command}")

        if not dry_run:
            result = subprocess.run(
                step.command,
                shell=True,
                cwd=workdir,
                check=False,
            )
            if result.returncode != 0:
                raise WorkflowExecutionError(
                    f"Step '{step.name}' failed with return code {result.returncode}"
                )

        if index != len(steps) and interval_seconds:
            print(f"等待 {interval_seconds}s 后执行下一步...\n")
            time.sleep(interval_seconds)

    print("\n工作流执行完成。")


def _ensure_directory(path: Path) -> None:
    """Ensure the working directory exists before execution."""

    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"工作目录不存在或不是目录: {path}")
