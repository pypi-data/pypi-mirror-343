import ast
import sys
from typing import Dict, List, Set


class AbsoluteImportChecker(ast.NodeVisitor):
    """检测相对导入的AST访问器"""

    def __init__(self):
        self.errors: List[str] = []

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """检测相对导入语句"""
        if node.level > 0:  # 相对导入(level > 0)
            error_msg = (
                f"F401: 第{node.lineno}行: "
                f"检测到相对导入 'from {'.'*node.level}{node.module}'"
            )
            self.errors.append(error_msg)
        self.generic_visit(node)


class ASTParser:
    """AST解析器，用于分析Python代码并识别错误模式"""
    
    name = 'flaekextens'
    version = '0.1.0'
    options = {}

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename
        self.error_codes: Dict[str, Set[str]] = {
            "P0": set(),
            "P1": set(),
            "P2": set()
        }
        self.error_descriptions: Dict[str, Dict[str, str]] = {
            "en": {},
            "zh": {}
        }
        self._results = []

    def __iter__(self):
        """实现迭代器接口，返回flake8格式的错误报告"""
        for result in self._results:
            yield result

    def register_error_code(
        self,
        code: str,
        category: str,
        en_desc: str = "",
        zh_desc: str = ""
    ) -> None:
        """注册错误码到指定分类并添加中英文描述
        Args:
            code: 错误码 (如F821)
            category: 错误分类 (P0/P1/P2)
            en_desc: 英文错误描述
            zh_desc: 中文错误描述
        """
        if category in self.error_codes:
            self.error_codes[category].add(code)
            if en_desc:
                self.error_descriptions["en"][code] = en_desc
            if zh_desc:
                self.error_descriptions["zh"][code] = zh_desc
    def parse_file(self, filepath: str) -> Dict[str, List[str]]:
        """解析Python文件并返回发现的错误"""
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        errors = {"P0": [], "P1": [], "P2": []}
        defined_vars = set()

        # 第一遍遍历：收集所有定义的变量、导入、类名和内置变量
        import builtins
        defined_vars.update(dir(builtins))

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defined_vars.update(arg.arg for arg in node.args.args)
                defined_vars.add(node.name)
            elif isinstance(node, ast.ClassDef):
                defined_vars.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_vars.add(target.id)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    defined_vars.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ''
                for alias in node.names:
                    defined_vars.add(alias.name)
                    if module:
                        defined_vars.add(
                            f"{module}.{alias.name}"
                        )
            elif (isinstance(node, ast.Name) and
                  isinstance(node.ctx, ast.Store)):
                defined_vars.add(node.id)
        
        # 第二遍遍历：检测未定义变量(F821)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                if (node.id not in defined_vars and
                    node.id not in dir(builtins)):
                    error_msg = (
                        f"F821: 第{node.lineno}行: "
                        f"未定义变量 '{node.id}'"
                    )
                    errors["P0"].append(error_msg)
        
        # 第三遍遍历：检测相对导入(F401)
        import_checker = AbsoluteImportChecker()
        import_checker.visit(tree)
        errors["P1"].extend(import_checker.errors)

        return errors


def main():
    parser = ASTParser()
    # 注册标准错误码及描述
    # P0级别错误码
    parser.register_error_code(
        "F821", "P0",
        "Undefined variable", "未定义变量"
    )
    parser.register_error_code(
        "F811", "P0",
        "Redefined unused variable", "重定义未使用变量"
    )
    parser.register_error_code(
        "F701", "P0",
        "Syntax error in forward annotation", "前向引用语法错误"
    )
    parser.register_error_code(
        "F704", "P0",
        "Invalid yield expression", "无效的yield表达式"
    )
    parser.register_error_code(
        "F705", "P0",
        "Invalid return statement", "无效的return语句"
    )
    parser.register_error_code(
        "F822", "P0",
        "Undefined name in __all__", "__all__中未定义名称"
    )
    parser.register_error_code(
        "F823", "P0",
        "Local variable referenced before assignment", "局部变量在赋值前被引用"
    )
    parser.register_error_code(
        "E999", "P0",
        "SyntaxError", "语法错误"
    )

    # P1级别错误码
    parser.register_error_code(
        "F401", "P1",
        "Module imported but unused", "导入模块但未使用"
    )
    parser.register_error_code(
        "F402", "P1",
        "Import shadowed by loop variable", "导入被循环变量覆盖"
    )
    parser.register_error_code(
        "F403", "P1",
        "Wildcard import", "通配符导入"
    )
    parser.register_error_code(
        "F841", "P1",
        "Local variable is assigned but never used", "局部变量被赋值但从未使用"
    )
    parser.register_error_code(
        "C901", "P1",
        "Function is too complex", "函数过于复杂"
    )
    parser.register_error_code(
        "F632", "P1",
        "Incorrect use of 'is' operator", "错误使用'is'运算符"
    )
    parser.register_error_code(
        "F633", "P1",
        "Incorrect use of 'not in' operator", "错误使用'not in'运算符"
    )
    parser.register_error_code(
        "F812", "P1",
        "List comprehension redefines variable", "列表推导式重定义变量"
    )
    parser.register_error_code(
        "F406", "P1",
        "Unused import from __future__", "未使用的__future__导入"
    )
    parser.register_error_code(
        "F702", "P1",
        "Redefined builtin", "重定义内置名称"
    )

    # P2级别错误码
    parser.register_error_code(
        "E231", "P2",
        "Missing whitespace after comma", "逗号后缺少空格"
    )
    parser.register_error_code(
        "E501", "P2",
        "Line too long", "行过长"
    )
    parser.register_error_code(
        "E225", "P2",
        "Missing whitespace around operator", "运算符周围缺少空格"
    )
    parser.register_error_code(
        "E302", "P2",
        "Expected 2 blank lines, found 0", "预期2个空行，发现0个"
    )
    parser.register_error_code(
        "E203", "P2",
        "Whitespace before colon", "冒号前有空格"
    )
    parser.register_error_code(
        "W291", "P2",
        "Trailing whitespace", "行尾空格"
    )
    parser.register_error_code(
        "E265", "P2",
        "Missing whitespace after #", "#后缺少空格"
    )
    parser.register_error_code(
        "E303", "P2",
        "Too many blank lines", "空行过多"
    )
    parser.register_error_code(
        "E127", "P2",
        "Continuation line over-indented", "续行缩进过多"
    )
    parser.register_error_code(
        "E128", "P2",
        "Continuation line under-indented", "续行缩进不足"
    )
# 调试输出已注册错误码
    print("\n已注册错误码:")
    for category, codes in parser.error_codes.items():
        print(f"{category}类错误码: {', '.join(codes)}")
        for code in codes:
            print(f"  {code}: {parser.error_descriptions['zh'][code]}")
    
    if len(sys.argv) < 2:
        print("请指定要分析的文件路径")
        return
    filepath = sys.argv[1]
    errors = parser.parse_file(filepath)

    print(f"分析文件: {filepath}")
    for category in ["P0", "P1", "P2"]:
        if errors[category]:
            print(f"\n{category}级别错误:")
            for error in errors[category]:
                print(f"  {error}")


def run(tree, filename):
    """flake8插件入口函数"""
    parser = ASTParser(tree, filename)

    # 注册所有标准错误码及描述
    # P0级别错误码
    # P0级别错误码
    parser.register_error_code(
        "F821", "P0",
        "Undefined variable", "未定义变量"
    )
    parser.register_error_code(
        "F811", "P0",
        "Redefined unused variable", "重定义未使用变量"
    )
    parser.register_error_code(
        "F701", "P0",
        "Syntax error in forward annotation", "前向引用语法错误"
    )
    parser.register_error_code(
        "F704", "P0",
        "Invalid yield expression", "无效的yield表达式"
    )
    parser.register_error_code(
        "F705", "P0",
        "Invalid return statement", "无效的return语句"
    )
    parser.register_error_code(
        "F822", "P0",
        "Undefined name in __all__", "__all__中未定义名称"
    )
    parser.register_error_code(
        "F823", "P0",
        "Local variable referenced before assignment",
        "局部变量在赋值前被引用"
    )
    parser.register_error_code(
        "E999", "P0",
        "SyntaxError", "语法错误"
    )
    
    # P1级别错误码
    parser.register_error_code(
        "F401", "P1",
        "Module imported but unused", "导入模块但未使用"
    )
    parser.register_error_code(
        "F402", "P1",
        "Import shadowed by loop variable", "导入被循环变量覆盖"
    )
    parser.register_error_code(
        "F403", "P1",
        "Wildcard import", "通配符导入"
    )
    parser.register_error_code(
        "F841", "P1",
        "Local variable is assigned but never used",
        "局部变量被赋值但从未使用"
    )
    parser.register_error_code(
        "C901", "P1",
        "Function is too complex", "函数过于复杂"
    )
    parser.register_error_code(
        "F632", "P1",
        "Incorrect use of 'is' operator", "错误使用'is'运算符"
    )
    parser.register_error_code(
        "F633", "P1",
        "Incorrect use of 'not in' operator",
        "错误使用'not in'运算符"
    )
    parser.register_error_code(
        "F812", "P1",
        "List comprehension redefines variable",
        "列表推导式重定义变量"
    )
    parser.register_error_code(
        "F406", "P1",
        "Unused import from __future__", "未使用的__future__导入"
    )
    parser.register_error_code(
        "F702", "P1",
        "Redefined builtin", "重定义内置名称"
    )
    
    # P2级别错误码
    parser.register_error_code(
        "E231", "P2",
        "Missing whitespace after comma", "逗号后缺少空格"
    )
    parser.register_error_code(
        "E501", "P2",
        "Line too long", "行过长"
    )
    parser.register_error_code(
        "E225", "P2",
        "Missing whitespace around operator", "运算符周围缺少空格"
    )
    parser.register_error_code(
        "E302", "P2",
        "Expected 2 blank lines, found 0", "预期2个空行，发现0个"
    )
    parser.register_error_code(
        "E203", "P2",
        "Whitespace before colon", "冒号前有空格"
    )
    parser.register_error_code(
        "W291", "P2",
        "Trailing whitespace", "行尾空格"
    )
    parser.register_error_code(
        "E265", "P2",
        "Missing whitespace after #", "#后缺少空格"
    )
    parser.register_error_code(
        "E303", "P2",
        "Too many blank lines", "空行过多"
    )
    parser.register_error_code(
        "E127", "P2",
        "Continuation line over-indented", "续行缩进过多"
    )
    parser.register_error_code(
        "E128", "P2",
        "Continuation line under-indented", "续行缩进不足"
    )
    
    # 执行分析
    errors = parser.parse_file(filename)

    # 转换为flake8格式的错误报告
    parser._results = []
    for category in ["P0", "P1", "P2"]:
        for error in errors[category]:
            code, msg = error.split(":", 1)
            line = int(msg.split("第")[1].split("行")[0])
            parser._results.append((
                line,  # 行号
                0,     # 列号
                f"{code.strip()} {msg.strip()}",  # 错误信息
                type('Flake8Error', (), {})  # 错误类型
            ))
    return parser

if __name__ == "__main__":
    main()
