from pathlib import Path
from typing import List


PYI_FILE = Path(__file__).parent / "__init__.pyi"
INIT_FILE = Path(__file__).parent / "__init__.py"

MARK_ALL = "# -- __all__"
MARK_STATIC_IMPORTS = "# -- static imports"
MARK_DYNAMIC_IMPORTS = "# -- dynamic imports"

LAZY_MODULE_IMPORT = "from instaui.systems.module_system import LazyModule"


def create_init_file():
    all_part_lines, static_lines, dynamic_lines = _split_by_marks(
        PYI_FILE, [MARK_ALL, MARK_STATIC_IMPORTS, MARK_DYNAMIC_IMPORTS]
    )

    # first line is comment, skip it
    dynamic_lines = [
        _conver_dynamic(line) for line in dynamic_lines[1:] if line.strip()
    ]

    with open(INIT_FILE, "w", encoding="utf-8") as f:
        f.writelines("\n".join(all_part_lines))
        f.write("\n")
        f.writelines("\n".join(static_lines))
        f.write("\n")

        f.writelines(
            "\n".join([MARK_DYNAMIC_IMPORTS, LAZY_MODULE_IMPORT, *dynamic_lines])
        )

    print(f"Create {INIT_FILE} success.")


def _split_by_marks(file: Path, marks: List[str]):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    marks_index = [lines.index(mark) for mark in marks]
    marks_index.append(len(lines))

    return [
        lines[marks_index[i] : marks_index[i + 1]] for i in range(len(marks_index) - 1)
    ]


def _conver_dynamic(dynamic_code: str):
    # "from instaui.components.highlight_code.code import Code as code" convert to "code = LazyModule('instaui.components.highlight_code.code', 'Code')"

    # instaui.components.highlight_code.code
    from_part = dynamic_code.split("import")[0][5:].strip()

    # Code as code
    import_part = dynamic_code.split("import")[1].strip()
    has_as = " as " in import_part

    member_name = ""
    alias_name = ""

    if has_as:
        member_name, alias_name = import_part.split(" as ")
    else:
        member_name = import_part
        alias_name = member_name

    return f"{alias_name} = LazyModule('{from_part}', '{member_name}')"


if __name__ == "__main__":
    create_init_file()
