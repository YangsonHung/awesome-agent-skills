import argparse
import os
from pathlib import Path
import glob
import sys
import curses
from datetime import datetime
import json

try:
    import readline
except ImportError:
    readline = None

from yuque_lakebook_export.lake_handle import sanitize_path_segment
from yuque_lakebook_export.lake_setup import start_convert


STATE_FILE = Path.home() / ".agents" / "state" / "yuque-lakebook-export.json"


def parse_bool(value):
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError("downloadImage 仅支持 True/False")


def load_state():
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state):
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def complete_path(text, state):
    expanded = os.path.expanduser(text or "")
    if not expanded:
        expanded = "."

    if os.path.isdir(expanded):
        pattern = os.path.join(expanded, "*")
    else:
        pattern = expanded + "*"

    matches = []
    for item in sorted(glob.glob(pattern)):
        display = item
        if os.path.isdir(item):
            display = os.path.join(item, "")
        if display.startswith(os.path.expanduser("~")):
            display = "~" + display[len(os.path.expanduser("~")):]
        matches.append(display)

    if state < len(matches):
        return matches[state]
    return None


def setup_readline():
    if readline is None:
        return
    doc = getattr(readline, "__doc__", "") or ""
    if "libedit" in doc.lower():
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(" \t\n;")
    readline.set_completer(complete_path)


def discover_lakebooks(search_dir):
    base_dir = Path(search_dir).expanduser().resolve()
    return sorted(base_dir.glob("*.lakebook"))


def parse_multi_select(raw_value, max_index):
    if not raw_value.strip():
        return []
    selected = set()
    for part in raw_value.split(","):
        item = part.strip()
        if not item:
            continue
        if "-" in item:
            start, end = item.split("-", 1)
            start_index = int(start.strip())
            end_index = int(end.strip())
            if start_index > end_index:
                start_index, end_index = end_index, start_index
            for index in range(start_index, end_index + 1):
                if 1 <= index <= max_index:
                    selected.add(index)
        else:
            index = int(item)
            if 1 <= index <= max_index:
                selected.add(index)
    return sorted(selected)


def toggle_select_all(selected_indexes, total_count):
    if len(selected_indexes) == total_count:
        return set()
    return set(range(total_count))


def draw_lakebook_selector(stdscr, lakebooks, cursor_index, selected_indexes, top_index):
    stdscr.erase()
    height, width = stdscr.getmaxyx()
    title = "请选择要执行的 .lakebook 文件"
    help_text = "↑↓移动  空格勾选/取消  a全选/取消全选  Enter确认  Ctrl+C退出"
    stdscr.addnstr(0, 0, title, width - 1)
    stdscr.addnstr(1, 0, help_text, width - 1)

    list_top = 3
    list_height = max(1, height - list_top - 1)
    visible_items = lakebooks[top_index:top_index + list_height]

    for offset, file_path in enumerate(visible_items):
        actual_index = top_index + offset
        marker = "[x]" if actual_index in selected_indexes else "[ ]"
        line = f"{marker} {file_path.name}"
        if actual_index == cursor_index:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addnstr(list_top + offset, 0, line, width - 1)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addnstr(list_top + offset, 0, line, width - 1)

    footer = f"已选择 {len(selected_indexes)} / {len(lakebooks)}"
    stdscr.addnstr(height - 1, 0, footer, width - 1)
    stdscr.refresh()


def curses_select_lakebooks(stdscr, lakebooks):
    curses.curs_set(0)
    stdscr.keypad(True)

    cursor_index = 0
    top_index = 0
    selected_indexes = set()

    while True:
        height, _ = stdscr.getmaxyx()
        list_height = max(1, height - 4)
        if cursor_index < top_index:
            top_index = cursor_index
        elif cursor_index >= top_index + list_height:
            top_index = cursor_index - list_height + 1

        draw_lakebook_selector(stdscr, lakebooks, cursor_index, selected_indexes, top_index)
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord('k')):
            cursor_index = (cursor_index - 1) % len(lakebooks)
        elif key in (curses.KEY_DOWN, ord('j')):
            cursor_index = (cursor_index + 1) % len(lakebooks)
        elif key == ord(' '):
            if cursor_index in selected_indexes:
                selected_indexes.remove(cursor_index)
            else:
                selected_indexes.add(cursor_index)
        elif key in (ord('a'), ord('A')):
            selected_indexes = toggle_select_all(selected_indexes, len(lakebooks))
        elif key in (10, 13, curses.KEY_ENTER):
            if selected_indexes:
                return [lakebooks[index] for index in sorted(selected_indexes)]
        elif key == 3:
            raise KeyboardInterrupt


def select_lakebooks_with_ui(lakebooks):
    try:
        return curses.wrapper(curses_select_lakebooks, lakebooks)
    except KeyboardInterrupt:
        print("\n已取消执行")
        sys.exit(130)
    except Exception:
        print("交互式勾选界面不可用，回退到编号输入模式")
        print("可选文件：")
        for idx, file_path in enumerate(lakebooks, 1):
            print(f"{idx}. {file_path.name}")
        raw_selection = safe_input("请选择文件编号，支持多选(例如 1,3-5): ").strip()
        selected_indexes = parse_multi_select(raw_selection, len(lakebooks))
        if not selected_indexes:
            print("未选择任何文件")
            return []
        return [lakebooks[index - 1] for index in selected_indexes]


def safe_input(prompt):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\n已取消执行")
        sys.exit(130)


def prompt_lakebooks(state):
    remembered_search_dir = state.get("last_search_dir")
    default_search_dir = Path(remembered_search_dir or Path.cwd())
    if remembered_search_dir:
        prompt = f"请输入待扫描目录(上次使用: {default_search_dir}，回车直接使用): "
    else:
        prompt = f"请输入待扫描目录(默认 {default_search_dir}): "
    search_dir_input = safe_input(prompt).strip()
    search_dir = search_dir_input or str(default_search_dir)
    lakebooks = discover_lakebooks(search_dir)
    if not lakebooks:
        print("未找到 .lakebook 文件")
        return [], None

    selected_lakebooks = select_lakebooks_with_ui(lakebooks)
    if not selected_lakebooks:
        print("未选择任何文件")
        return [], None
    return selected_lakebooks, Path(search_dir).expanduser().resolve()


def prompt_output_root(default_root, state):
    remembered_output_root = state.get("last_output_root")
    if remembered_output_root:
        default_root = Path(remembered_output_root)
        prompt = f"目标根目录(上次使用: {default_root}，回车直接使用): "
    else:
        prompt = f"目标根目录(默认 {default_root}): "
    output_root_input = safe_input(prompt).strip()
    return Path(output_root_input).expanduser() if output_root_input else default_root


def prompt_open_output(default_value=False, state=None):
    if state is not None:
        default_value = bool(state.get("last_open_output", default_value))
    hint = "y/N" if not default_value else "Y/n"
    if state is not None and "last_open_output" in state:
        last_value = "是" if default_value else "否"
        prompt = f"导出成功后是否自动打开目标目录？(上次使用: {last_value})[{hint}]: "
    else:
        prompt = f"导出成功后是否自动打开目标目录？[{hint}]: "
    raw_value = safe_input(prompt).strip().lower()
    if not raw_value:
        return default_value
    return raw_value in {"y", "yes"}


def build_output_dir(output_root, lakebook_path):
    stem = sanitize_path_segment(lakebook_path.stem)
    return output_root / stem


def get_log_output_dir(lakebooks):
    if not lakebooks:
        return None
    parent_dirs = [str(Path(lakebook).expanduser().resolve().parent) for lakebook in lakebooks]
    common_dir = os.path.commonpath(parent_dirs)
    return Path(common_dir)


def run_batch(lakebooks, output_root, download_image, skip_existing, open_output=False):
    output_root = output_root.expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    batch_results = []
    for lakebook in lakebooks:
        target_dir = build_output_dir(output_root, lakebook)
        print(f"\n>>> 开始处理: {lakebook}")
        print(f">>> 输出目录: {target_dir}")
        result = start_convert(None, str(lakebook), str(target_dir), download_image, skip_existing, open_output=open_output)
        batch_results.append({
            "lakebook": str(lakebook),
            "target_dir": str(target_dir),
            **(result or {})
        })
        if result and not result.get("success"):
            print(f">>> 当前文件处理失败，继续下一个: {lakebook}")
    log_dir = get_log_output_dir(lakebooks)
    log_path = write_batch_log(batch_results, log_dir)
    print_batch_summary(batch_results)
    if log_path:
        print(f">>> 执行日志: {log_path}")


def print_batch_summary(batch_results):
    if not batch_results:
        return
    success_results = [item for item in batch_results if item.get("success")]
    failed_results = [item for item in batch_results if not item.get("success")]

    print("\n>>> 批量执行完成")
    print(f">>> 成功: {len(success_results)}  失败: {len(failed_results)}")

    if success_results:
        print(">>> 成功列表：")
        for item in success_results:
            print(f"- {item['lakebook']} -> {item['target_dir']} (导出 {item.get('file_count', 0)} 个文件)")

    if failed_results:
        print(">>> 失败列表：")
        for item in failed_results:
            print(f"- {item['lakebook']} -> {item['target_dir']}")
            print(f"  错误: {item.get('error') or '未知错误'}")


def write_batch_log(batch_results, log_dir):
    if not batch_results or log_dir is None:
        return None
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"yuque-export-{timestamp}.log"
    lines = [
        f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"成功数量: {len([item for item in batch_results if item.get('success')])}",
        f"失败数量: {len([item for item in batch_results if not item.get('success')])}",
        ""
    ]

    for item in batch_results:
        lines.append(f"源文件: {item.get('lakebook')}")
        lines.append(f"输出目录: {item.get('target_dir')}")
        lines.append(f"执行结果: {'成功' if item.get('success') else '失败'}")
        lines.append(f"导出文件数: {item.get('file_count', 0)}")
        if item.get("error"):
            lines.append(f"错误信息: {item.get('error')}")
        if item.get("traceback"):
            lines.append("错误堆栈:")
            lines.append(item.get("traceback", "").rstrip())
        lines.append("-" * 60)

    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return log_path


def preview_batch(lakebooks, output_root):
    print("\n即将执行以下任务：")
    for lakebook in lakebooks:
        target_dir = build_output_dir(output_root, lakebook)
        print(f"- {lakebook} -> {target_dir}")


def confirm_execution():
    confirm = safe_input("确认开始执行？[Y/n]: ").strip().lower()
    return confirm in {"", "y", "yes"}


def run_interactive(download_image, skip_existing, open_output=False):
    state = load_state()
    lakebooks, search_dir = prompt_lakebooks(state)
    if not lakebooks:
        return
    output_root = prompt_output_root(search_dir, state)
    open_output = prompt_open_output(default_value=open_output, state=state)
    preview_batch(lakebooks, output_root)
    if not confirm_execution():
        print("已取消执行")
        return
    run_batch(lakebooks, output_root, download_image, skip_existing, open_output=open_output)
    save_state({
        "last_search_dir": str(search_dir),
        "last_output_root": str(output_root.expanduser().resolve()),
        "last_open_output": open_output
    })


if __name__ == '__main__':
    setup_readline()
    parser = argparse.ArgumentParser(
        description="Export one or more Yuque .lakebook files into local Markdown folders for Obsidian."
    )
    parser.add_argument('-i', '--meta', help="lake文件的meta.json路径", type=str)
    parser.add_argument('-l', '--lake', help="lakebook文件路径，支持多个", nargs='*')
    parser.add_argument('-o', '--output', help="生成markdown的根路径", type=str)
    parser.add_argument('-d', '--downloadImage', help="是否下载图片", type=parse_bool, default=True)
    parser.add_argument('-s', '--skip-existing-resources', help="是否跳过本地已存在的图片和附件文件", action='store_true')
    parser.add_argument('--open-output', help="导出成功后自动打开目标目录", action='store_true')
    parser.add_argument('--interactive', help="启用交互式选择", action='store_true')
    args = parser.parse_args()

    is_interactive_mode = args.interactive or (not args.meta and not args.lake)
    if is_interactive_mode:
        run_interactive(args.downloadImage, args.skip_existing_resources, open_output=args.open_output)
    elif args.meta:
        start_convert(args.meta, None, args.output, args.downloadImage, args.skip_existing_resources,
                      open_output=args.open_output)
    else:
        lakebooks = [Path(item).expanduser().resolve() for item in args.lake]
        if len(lakebooks) == 1 and args.output:
            output_root = Path(args.output).expanduser()
            target_dir = build_output_dir(output_root, lakebooks[0])
            start_convert(None, str(lakebooks[0]), str(target_dir), args.downloadImage, args.skip_existing_resources,
                          open_output=args.open_output)
        else:
            default_output_root = lakebooks[0].parent if lakebooks else Path.cwd()
            output_root = Path(args.output).expanduser() if args.output else default_output_root
            run_batch(lakebooks, output_root, args.downloadImage, args.skip_existing_resources,
                      open_output=args.open_output)
