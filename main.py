"""AI packet automation tool entry point.

Usage examples:
  python main.py --workdir /TSN源码R/data
  python main.py --interval 10 --dry-run
"""

from __future__ import annotations

import argparse

from src.ai_packet_tool.command_runner import WorkflowExecutionError, run_steps
from src.ai_packet_tool.workflow import WorkflowConfig, build_default_steps, resolve_workdir


def parse_args() -> argparse.Namespace:
    """Parse CLI parameters."""

    parser = argparse.ArgumentParser(
        description="AI抓包自动化工具：自动执行抓包、解析、分析步骤",
    )
    parser.add_argument("--workdir", help="命令执行目录；默认当前目录")
    parser.add_argument("--interval", type=int, default=10, help="步骤间隔秒数，默认10")
    parser.add_argument("--interface", default="enp1s0", help="抓包网卡名称")
    parser.add_argument("--source-ip", default="192.168.0.21", help="抓包来源IP")
    parser.add_argument("--packet-count", type=int, default=60000, help="抓包数量")
    parser.add_argument("--pcap-file", default="tmp_21.pcap", help="输出pcap文件名")
    parser.add_argument("--out-file", default="tmp_21.out", help="输出文本文件名")
    parser.add_argument(
        "--analysis-cmd",
        default="./txtime_offset_stats.py -f tmp_21.out",
        help="分析脚本命令",
    )
    parser.add_argument("--dry-run", action="store_true", help="仅打印命令，不实际执行")
    return parser.parse_args()


def main() -> int:
    """Program entry function."""

    args = parse_args()
    config = WorkflowConfig(
        interface=args.interface,
        source_ip=args.source_ip,
        packet_count=args.packet_count,
        pcap_file=args.pcap_file,
        out_file=args.out_file,
        python_analysis_cmd=args.analysis_cmd,
    )

    steps = build_default_steps(config)
    workdir = resolve_workdir(args.workdir)

    try:
        run_steps(
            steps=steps,
            interval_seconds=args.interval,
            workdir=workdir,
            dry_run=args.dry_run,
        )
    except (WorkflowExecutionError, FileNotFoundError, ValueError) as exc:
        print(f"执行失败: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
