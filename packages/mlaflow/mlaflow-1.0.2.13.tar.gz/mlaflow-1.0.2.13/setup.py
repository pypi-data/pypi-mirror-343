import os
from setuptools import setup, find_packages

# 获取当前文件夹路径
here = os.path.abspath(os.path.dirname(__file__))

# 读取 README.md 文件作为 long_description
with open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

# 设置版本和描述
VERSION = '1.0.2.13'
DESCRIPTION = 'A package for unsupervised and fully automatic processing of single-cell sequencing data throughout the entire workflow.'

setup(
    name="mlaflow",
    version=VERSION,
    author="jianing kang",
    author_email="U202342138@xs.ustb.edu.cn",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",  # Markdown 格式
    packages=find_packages(),  # 自动查找所有包,
    install_requires=[
        'scanpy>=1.7.2',
        'optuna>=2.8.0',
        'cma>=3.0',
        'umap-learn>=0.5.1',
    ],
    keywords=['python', 'mlaflow', 'MLAflow', 'single-cell', 'scRNA-seq', 'bioinformatics', 'machine learning'],
    classifiers=[
        "Development Status :: 4 - Beta",  # 更新开发状态
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ]
)
