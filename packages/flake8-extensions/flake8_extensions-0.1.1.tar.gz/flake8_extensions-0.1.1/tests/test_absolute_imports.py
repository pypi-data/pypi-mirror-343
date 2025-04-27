import ast
import pytest
from flaekextens.plugin import AbsoluteImportChecker

def test_relative_import_detection():
    """测试相对导入检测"""
    code = """
from . import module
from ..parent import func
from ...grandparent import Class
    """
    tree = ast.parse(code)
    checker = AbsoluteImportChecker()
    checker.visit(tree)
    
    assert len(checker.errors) == 3
    assert "IA001" in checker.errors[0]
    assert "当前层级: 1" in checker.errors[0]
    assert "当前层级: 2" in checker.errors[1]
    assert "当前层级: 3" in checker.errors[2]

def test_absolute_import_allowed():
    """测试绝对导入不报错"""
    code = """
from package import module
from package.sub import func
    """
    tree = ast.parse(code)
    checker = AbsoluteImportChecker()
    checker.visit(tree)
    
    assert len(checker.errors) == 0