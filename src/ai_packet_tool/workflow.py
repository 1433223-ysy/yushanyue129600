"""Workflow generation logic for packet capture, conversion, and analysis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .command_runner import WorkflowStep


@dataclass(frozen=True)
class WorkflowConfig:
    """Configurable parameters for packet processing workflow."""

    interface: str = "enp1s0"
    source_ip: str = "192.168.0.21"
    packet_count: int = 60000
    pcap_file: str = "tmp_21.pcap"
    out_file: str = "tmp_21.out"
    python_analysis_cmd: str = "./txtime_offset_stats.py -f tmp_21.out"


def build_default_steps(config: WorkflowConfig) -> list[WorkflowStep]:
    """Build workflow steps based on user config.

    The commands are aligned with the screenshot provided by the user:
      1) tcpdump capture
      2) tshark extraction and output redirect
      3) python analysis script
    """

    pcap_path = config.pcap_file
    out_path = config.out_file

    capture_cmd = (
        "sudo tcpdump "
        f"-c {config.packet_count} "
        f"-i {config.interface} "
        f"src {config.source_ip} "
        f"-w {pcap_path} "
        "-j adapter_unsynced "
        "-tt "
        "--time-stamp-precision=nano"
    )

    tshark_cmd = (
        f"tshark -r {pcap_path} "
        "--disable-protocol dcp-etsi "
        "--disable-protocol dcp-pft "
        "-t e "
        "-E separator=, "
        "-T fields "
        "-e frame.number "
        "-e frame.time_epoch "
        "-e data.data "
        f"> {out_path}"
    )

    return [
        WorkflowStep(name="抓包保存为 PCAP", command=capture_cmd),
        WorkflowStep(name="PCAP 转换为文本输出", command=tshark_cmd),
        WorkflowStep(name="运行时延偏移分析脚本", command=config.python_analysis_cmd),
    ]


def resolve_workdir(workdir: str | None) -> Path:
    """Resolve work directory; default to current process directory."""

    return Path(workdir).expanduser().resolve() if workdir else Path.cwd()
