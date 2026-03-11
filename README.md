# AI 抓包自动化工具

该工具用于在 Linux 工控机场景中，按固定流程自动执行：
1. `tcpdump` 抓包保存；
2. `tshark` 解析输出；
3. Python 脚本分析；
并在每一步之间自动等待 10 秒（可配置）。

## 功能说明

- 支持在当前终端目录执行，或通过 `--workdir` 指定目录执行。
- 内置默认命令参数，和你给出的图片流程一致。
- 通过参数可灵活调整网卡、来源 IP、抓包数量、输出文件、分析命令。
- 支持 `--dry-run` 预览命令，不实际执行，便于调试。
- 结构化代码与完整注释，便于后续维护。

## 项目结构

```text
.
├── main.py                        # 程序入口
├── build_exe.sh                   # 一键打包脚本（PyInstaller）
└── src/ai_packet_tool/
    ├── command_runner.py          # 步骤执行与错误处理
    ├── workflow.py                # 工作流命令构建
    └── __init__.py
```

## 运行方式

### 1) 本地 Python 运行

```bash
python main.py --workdir /TSN源码R/data
```

### 2) 仅预览（不执行）

```bash
python main.py --dry-run --workdir /TSN源码R/data
```

### 3) 常用参数示例

```bash
python main.py \
  --workdir /TSN源码R/data \
  --interval 10 \
  --interface enp1s0 \
  --source-ip 192.168.0.21 \
  --packet-count 60000 \
  --pcap-file tmp_21.pcap \
  --out-file tmp_21.out \
  --analysis-cmd "./txtime_offset_stats.py -f tmp_21.out"
```

## 在 Linux 上运行 `build_exe.sh` 需要怎么配置

> 注：Linux 上扩展名通常不要求 `.exe`，本项目按需求输出 `ai_packet_tool.exe`。

### 1) 基础系统依赖

Debian/Ubuntu：

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv build-essential
```

RHEL/CentOS：

```bash
sudo dnf install -y python3 python3-pip python3-virtualenv gcc
```

### 2) 建议使用虚拟环境（避免污染系统 Python）

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install pyinstaller
```

### 3) 执行打包

```bash
./build_exe.sh
```

如果你想指定 Python 版本（例如 python3.10）：

```bash
./build_exe.sh python3.10
```

打包完成后文件位于：

```text
dist/ai_packet_tool.exe
```

### 4) 常见问题

- **报错 `PyInstaller is not installed`**：当前环境缺少 PyInstaller，执行 `python -m pip install pyinstaller`。
- **目标机运行失败（GLIBC 版本不兼容）**：
  - 应在“更老或相同版本”Linux 系统上打包，再拷贝到工控机；
  - 或直接在工控机同版本环境内打包，兼容性最好。
- **权限问题**：执行 `chmod +x dist/ai_packet_tool.exe` 后再运行。

## 默认执行命令（与图片步骤对齐）

1. 抓包：

```bash
sudo tcpdump -c 60000 -i enp1s0 src 192.168.0.21 -w tmp_21.pcap -j adapter_unsynced -tt --time-stamp-precision=nano
```

2. 解析：

```bash
tshark -r tmp_21.pcap --disable-protocol dcp-etsi --disable-protocol dcp-pft -t e -E separator=, -T fields -e frame.number -e frame.time_epoch -e data.data > tmp_21.out
```

3. 分析：

```bash
./txtime_offset_stats.py -f tmp_21.out
```

## 维护建议

- 如果将来新增步骤，可在 `src/ai_packet_tool/workflow.py` 中扩展 `build_default_steps`。
- 如果要接入 GUI 或 Web，仅需复用 `run_steps` 与 `WorkflowConfig`，替换入口层即可。
