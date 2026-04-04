# -*- coding: utf-8 -*-
"""
@Time ： 2023年11月13日 13点41分
@Auth ： zhoup
@File ：lake_setup.py
"""
import json
import re
import traceback

import yaml
import os
import shutil
import tempfile
from yuque_lakebook_export.lake_handle import MyParser, MyContext, remove_invalid_characters, sanitize_path_segment
from yuque_lakebook_export.lake_reader import unpack_lake_book_file


class GlobalContext:
    def __init__(self):
        # parent_id和book
        self.parent_id_and_child = {}
        # 将id和book映射起来
        self.id_and_book = {}
        # 存放根目录的book
        self.root_books = []
        self.file_count = 0
        self.all_file_count = 0
        self.failure_image_download_list = []
        self.file_total = 0
        self.total = 0
        self.download_image = True
        self.skip_existing = False
        self.root_path = ""
        self.doc_path_map = {}


HEADING_RE = re.compile(r'^\s{0,3}#{1,6}\s+')
HR_RE = re.compile(r'^\s{0,3}([-*_])(\s*\1){2,}\s*$')
TABLE_ROW_RE = re.compile(r'^\s*\|.*\|\s*$')
LIST_RE = re.compile(r'^\s*(?:[-+*]|\d+\.)\s+')
LAKE_PREFIX_RE = re.compile(r'^\ufeff?lake(?=\s*<)', re.IGNORECASE)
LAKE_MD_PREFIX_RE = re.compile(r'^\ufeff?lake(?=\s{0,3}#{1,6}\s)', re.IGNORECASE)


def normalize_markdown(text):
    """
    统一整理块级元素之间的空行，提升 Obsidian 等 Markdown 渲染兼容性。
    """
    text = text.lstrip("\ufeff")
    text = LAKE_MD_PREFIX_RE.sub("", text, count=1)
    lines = text.splitlines()
    if not lines:
        return text

    normalized = []
    in_fence = False

    def is_blank(value):
        return value.strip() == ""

    def is_fence(value):
        stripped = value.strip()
        return stripped.startswith("```") or stripped.startswith("~~~")

    def is_heading(value):
        return bool(HEADING_RE.match(value))

    def is_hr(value):
        return bool(HR_RE.match(value))

    def is_table_row(value):
        return bool(TABLE_ROW_RE.match(value))

    def previous_nonblank():
        for item in reversed(normalized):
            if not is_blank(item):
                return item
        return None

    for index, line in enumerate(lines):
        stripped = line.rstrip()
        next_line = lines[index + 1] if index + 1 < len(lines) else ""
        prev = previous_nonblank()
        current_is_fence = is_fence(stripped)
        current_is_heading = is_heading(stripped)
        current_is_hr = is_hr(stripped)
        current_is_table = is_table_row(stripped)
        next_is_table = is_table_row(next_line)

        if not in_fence:
            should_prepend_blank = False
            if current_is_heading or current_is_hr or current_is_fence:
                should_prepend_blank = prev is not None
            elif current_is_table and prev is not None and not is_table_row(prev):
                should_prepend_blank = True

            if should_prepend_blank and normalized and not is_blank(normalized[-1]):
                normalized.append("")

        normalized.append(stripped)

        if current_is_fence:
            in_fence = not in_fence
            if not in_fence and next_line and next_line.strip() and not is_blank(next_line):
                if not is_blank(normalized[-1]):
                    normalized.append("")
            continue

        if in_fence:
            continue

        if current_is_table and not next_is_table:
            if next_line and next_line.strip():
                normalized.append("")
        elif (current_is_heading or current_is_hr) and next_line and next_line.strip():
            normalized.append("")

    collapsed = []
    blank_count = 0
    for line in normalized:
        if is_blank(line):
            blank_count += 1
            if blank_count > 1:
                continue
        else:
            blank_count = 0
        collapsed.append(line)

    result = "\n".join(collapsed).strip() + "\n"
    return result


# from lxml import etree
def load_meta_json(global_context: GlobalContext):
    """
    解析meta.json中标注的文件关系
    :return:
    """
    full_path = "/".join([global_context.root_path, "$meta.json"])
    fp = open(full_path, 'r', encoding='utf-8')
    json_obj = json.load(fp)
    meta = json_obj['meta']
    # print(meta)
    meta_obj = json.loads(meta)
    book_yml = meta_obj['book']['tocYml']
    # print(book_yml)
    # with open('meta_book_yml.yaml', 'w+', encoding='utf-8') as yaml_fp:
    #     yaml_fp.write(book_yml)
    #     yaml_fp.flush()
    books = yaml.load(book_yml, yaml.Loader)
    for book in books:
        if book.get('uuid'):
            global_context.id_and_book[book['uuid']] = book
        if book['type'] == 'META':
            continue
        if book['parent_uuid'] == '':
            global_context.root_books.append(book)
            continue
        parent_uuid = book['parent_uuid']
        if global_context.parent_id_and_child.get(parent_uuid):
            global_context.parent_id_and_child[parent_uuid].append(book)
        else:
            global_context.parent_id_and_child[parent_uuid] = []
            global_context.parent_id_and_child[parent_uuid].append(book)
    # print(books)
    global_context.file_total = len(global_context.id_and_book)
    global_context.total = len(global_context.id_and_book)


def create_tree_dir(global_context, parent_dir, book):
    """
    根据解析出的关系创建文档的目录树
    :param parent_dir: 当前文档所在的父目录
    :param book: 当前book对象
    :param global_context 上下文
    :return:
    """
    if book is None:
        return
    uuid = book['uuid']
    name = sanitize_path_segment(book['title'])
    file_url = book['url']
    book_children = global_context.parent_id_and_child.get(uuid)
    has_children = bool(book_children)
    current_dir = parent_dir

    if has_children or file_url == '':
        current_dir = remove_invalid_characters(os.path.join(parent_dir, name))
        if not os.path.exists(current_dir):
            os.makedirs(current_dir, exist_ok=True)

    global_context.all_file_count += 1
    if file_url != '':
        ltm = LakeToMd(
            os.path.join(global_context.root_path, "{}.json".format(file_url)),
            target=os.path.join(current_dir if has_children else parent_dir, name)
        )
        ltm.to_md(global_context)
        global_context.failure_image_download_list += ltm.image_download_failure
        global_context.file_count += 1
        # print("\r", end="")
        # i = (file_count // file_total) * 100
        print("\rprocess progress: {}/{}/{}. ".format(global_context.file_count, global_context.all_file_count,
                                                      global_context.file_total), end="")
        # sys.stdout.flush()
        # time.sleep(0.05)
    if not book_children:
        return
    for child in book_children:
        create_tree_dir(global_context, current_dir, child)


def register_doc_paths(global_context, parent_dir, book):
    """
    预先计算所有导出 markdown 路径，供内部文档链接转相对路径使用。
    """
    if book is None:
        return
    uuid = book['uuid']
    name = sanitize_path_segment(book['title'])
    file_url = book['url']
    book_children = global_context.parent_id_and_child.get(uuid)
    has_children = bool(book_children)
    current_dir = parent_dir

    if has_children or file_url == '':
        current_dir = remove_invalid_characters(os.path.join(parent_dir, name))

    if file_url != '':
        target_base = os.path.join(current_dir if has_children else parent_dir, name)
        target_md_path = remove_invalid_characters(target_base) + ".md"
        global_context.doc_path_map[uuid] = target_md_path
        global_context.doc_path_map[file_url] = target_md_path
        if book.get('doc_id') is not None:
            global_context.doc_path_map[str(book['doc_id'])] = target_md_path

    if not book_children:
        return
    for child in book_children:
        register_doc_paths(global_context, current_dir, child)


class LakeToMd:
    body_html = None
    image_download_failure = []

    def __init__(self, filename, target):
        self.filename = filename
        self.target = target
        self.__body_html()

    def __body_html(self):
        fp = open(file=self.filename, mode='r', encoding='utf-8')
        file_json = json.load(fp)
        fp.close()
        self.body_html = self._extract_body(file_json)

    @staticmethod
    def _extract_body(file_json):
        doc_json = file_json.get("doc") or {}
        body_fields = (
            "body_draft_asl",
            "body_asl",
            "body_draft",
            "body",
        )
        for field in body_fields:
            body = doc_json.get(field)
            if isinstance(body, str) and body.strip():
                return LakeToMd._normalize_body(body)
        return ""

    @staticmethod
    def _normalize_body(body):
        """
        Some lakebook documents retain a Yuque Lake format marker at the beginning,
        for example `lake<h2>...`. Strip the accidental prefix so it does not render
        as `lake##` in the exported Markdown.
        """
        cleaned = body.lstrip("\ufeff")
        cleaned = LAKE_PREFIX_RE.sub("", cleaned, count=1)
        return cleaned

    def to_md(self, global_context):
        mp = MyParser(self.body_html)
        name = os.path.basename(self.target)
        short_target = os.path.dirname(self.target)
        current_file_path = remove_invalid_characters(self.target) + ".md"
        if short_target and not os.path.exists(short_target):
            os.makedirs(short_target, exist_ok=True)
        context = MyContext(
            filename=name,
            image_target=short_target,
            download_image=global_context.download_image,
            skip_existing=global_context.skip_existing,
            current_file_path=current_file_path,
            doc_path_map=global_context.doc_path_map
        )
        res = mp.handle_descent(mp.soup, context)
        res = normalize_markdown(res)
        self.image_download_failure += context.failure_images
        self.target = remove_invalid_characters(self.target)
        if not res.strip():
            print(f"\n警告: 文档导出结果为空 -> {self.filename}")
        with open(self.target + ".md", 'w+', encoding='utf-8') as fp:
            fp.writelines(res)
            fp.flush()


def convert_to_md(global_context, file_path, open_output=False):
    output_path = file_path
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
    global_context.doc_path_map = {}
    for root_book in global_context.root_books:
        register_doc_paths(global_context, output_path, root_book)
    for root_book in global_context.root_books:
        create_tree_dir(global_context, output_path, root_book)
    print("\n>>> markdown 转换完成")
    if open_output:
        # 根据操作系统选择合适的命令打开文件夹
        import platform
        system = platform.system()
        if system == 'Windows':
            os.system("explorer " + output_path)
        elif system == 'Darwin':  # macOS
            os.system("open " + output_path)
        elif system == 'Linux':
            os.system("xdg-open " + output_path)
        else:
            print("未识别的操作系统，无法自动打开输出文件夹")


def start_convert(meta, lake_book, output, download_image_of_in, skip_existing=False, open_output=False):
    global_context = GlobalContext()
    temp_dir = tempfile.mkdtemp(prefix="yuque_export_")
    result = {
        "success": False,
        "file_count": 0,
        "output": os.path.abspath(output) if output else output,
        "error": None,
        "failure_images": []
    }
    if lake_book:
        global_context.root_path = unpack_lake_book_file(lake_book, temp_dir)
        print(">>> lake文件抽取完成")
    else:
        global_context.root_path = meta
    if not global_context.root_path:
        print("参数校验失败！-i或者-l二者必须有一个")
        result["error"] = "参数校验失败！-i或者-l二者必须有一个"
        return result
    try:
        load_meta_json(global_context)
        print(">>> meta json解析完成")
        global_context.download_image = download_image_of_in
        global_context.skip_existing = skip_existing
        abspath = os.path.abspath(output)
        print(">>> 开始进行markdown转换")
        convert_to_md(global_context, abspath, open_output=open_output)
        print("共导出%s个文件" % global_context.file_count)

        print("图片下载错误列表:")
        print(' list: ', global_context.failure_image_download_list)
        print(' count:', len(global_context.failure_image_download_list))
        result["success"] = True
        result["file_count"] = global_context.file_count
        result["failure_images"] = list(global_context.failure_image_download_list)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    except Exception as e:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        print(e)
        result["error"] = str(e)
        result["traceback"] = traceback.format_exc()
    return result
# """
# 已经完成到根据meta生成目录了
# """
# if __name__ == '__main__':
#     load_meta_json('data/$.meta.json')
#     file_total = len(id_and_book)
#     total = len(id_and_book)
#     abspath = os.path.abspath("test")
#     convert_to_md(abspath)
#     print("共导出%s个文件" % file_count)
#
#     print("图片下载错误列表:")
#     print(failure_image_download_list)
#     parse_failure_result(failure_image_download_list)
