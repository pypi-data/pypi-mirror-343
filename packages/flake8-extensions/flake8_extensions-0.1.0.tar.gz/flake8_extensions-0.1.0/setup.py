from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='flaekextens',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='Flake8 extension for custom error codes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/flaekextens',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'flake8>=3.0.0',
    ],
    entry_points={
        'flake8.extension': [
            'F8 = flaekextens.main:ASTParser',
        ],
    },
    flake8_error_codes={
        'F821': {'en': 'undefined name', 'zh': '未定义变量', 'severity': 'error'},
        'F811': {'en': 'redefinition of unused name', 'zh': '重复定义未使用的变量', 'severity': 'error'},
        'F701': {'en': 'syntax error', 'zh': '语法错误', 'severity': 'error'},
        'F704': {'en': 'invalid syntax in starred expression', 'zh': '星号表达式语法错误', 'severity': 'error'},
        'F705': {'en': 'invalid syntax in yield expression', 'zh': 'yield表达式语法错误', 'severity': 'error'},
        'F822': {'en': 'undefined name in __all__', 'zh': '__all__中未定义变量', 'severity': 'error'},
        'F823': {'en': 'local variable referenced before assignment', 'zh': '局部变量在赋值前引用', 'severity': 'error'},
        'E999': {'en': 'syntax error (compile-time)', 'zh': '编译时语法错误', 'severity': 'error'},
        'F401': {'en': 'unused import', 'zh': '未使用的导入', 'severity': 'warning'},
        'F402': {'en': 'import shadowed by loop variable', 'zh': '导入被循环变量覆盖', 'severity': 'warning'},
        'F403': {'en': 'wildcard import', 'zh': '通配符导入', 'severity': 'warning'},
        'F841': {'en': 'unused local variable', 'zh': '未使用的局部变量', 'severity': 'warning'},
        'C901': {'en': 'function too complex', 'zh': '函数过于复杂', 'severity': 'warning'},
        'F632': {'en': 'invalid is/is not comparison', 'zh': '无效的is/is not比较', 'severity': 'warning'},
        'F633': {'en': 'invalid in/not in comparison', 'zh': '无效的in/not in比较', 'severity': 'warning'},
        'F812': {'en': 'list comprehension redefines variable', 'zh': '列表推导式重定义变量', 'severity': 'warning'},
        'F406': {'en': 'invalid from ... import * target', 'zh': '无效的from...import *目标', 'severity': 'warning'},
        'F702': {'en': 'invalid syntax in assignment', 'zh': '赋值语句语法错误', 'severity': 'warning'},
        'E231': {'en': 'missing whitespace after comma', 'zh': '逗号后缺少空格', 'severity': 'style'},
        'E501': {'en': 'line too long', 'zh': '行过长', 'severity': 'style'},
        'E225': {'en': 'missing whitespace around operator', 'zh': '操作符周围缺少空格', 'severity': 'style'},
        'E302': {'en': 'expected blank lines between functions', 'zh': '函数间缺少空行', 'severity': 'style'},
        'E203': {'en': 'whitespace before colon', 'zh': '冒号前有空格', 'severity': 'style'},
        'W291': {'en': 'trailing whitespace', 'zh': '行尾空格', 'severity': 'style'},
        'E265': {'en': 'missing whitespace after #', 'zh': '注释#后缺少空格', 'severity': 'style'},
        'E303': {'en': 'too many blank lines', 'zh': '空行过多', 'severity': 'style'},
        'E127': {'en': 'continuation line over-indented', 'zh': '续行缩进过多', 'severity': 'style'},
        'E128': {'en': 'continuation line under-indented', 'zh': '续行缩进不足', 'severity': 'style'}
    }
)