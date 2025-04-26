# 使用 python -m build 编译
# 然后使用 twine upload dist/* 上传到pypi
from setuptools import setup, find_packages
import os

def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'YkPywebview', 'version.py')
    with open(version_file, 'r') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="YkPywebview",
    version=get_version(),
    author="Yang Ke",
    author_email="540673597@qq.com",
    description="A wrapper library for pywebview with enhanced features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/yangke02/yk-pywebview",
    packages=['YkPywebview'],
    package_dir={'YkPywebview': 'YkPywebview'},
    install_requires=[
        "pywebview>=3.0"
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
