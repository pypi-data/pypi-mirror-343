import ast
from typing import Any, Generator, List, Tuple, Type


class AbsoluteImportChecker:
    """检测相对导入的Flake8插件"""
    name = "flake8-absolute-imports"
    version = "1.0.0"

    def __init__(self, tree: ast.AST, filename: str):
        self.tree = tree
        self.filename = filename

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        """Flake8插件入口方法"""
        visitor = ImportFromVisitor()
        visitor.visit(self.tree)
        for lineno, col_offset, message in visitor.errors:
            yield lineno, col_offset, message, type(self)


class ImportFromVisitor(ast.NodeVisitor):
    """检测相对导入的AST访问器"""
    
    def __init__(self):
        self.errors: List[Tuple[int, int, str]] = []

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """检测相对导入语句"""
        if node.level > 0:  # 相对导入(level > 0)
            message = (
                f"IA001 禁止使用相对路径导入，请改为绝对路径（当前层级: {node.level}）"
            )
            self.errors.append((node.lineno, node.col_offset, message))
        self.generic_visit(node)