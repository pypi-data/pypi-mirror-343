# 使用 python -m build 编译
# 然后使用 twine upload dist/* 上传到pypi
from setuptools import setup, find_packages
__version__ = "25.4.1"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="YkPywebview",
    version=__version__,
    author="Yang Ke",
    author_email="540673597@qq.com",
    description="A wrapper library for pywebview with enhanced features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/yangke02/yk-pywebview",
    packages=find_packages(),
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
