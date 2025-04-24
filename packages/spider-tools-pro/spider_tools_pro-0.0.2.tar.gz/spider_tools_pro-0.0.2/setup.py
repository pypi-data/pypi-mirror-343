from setuptools import setup, find_packages
import os
import sys


setup(
    name="spider-tools-pro",
    version="0.0.2",
    author="MindLullaby",
    author_email="3203939025@qq.com",
    description="A professional spider tools package",
    url="https://github.com/6210qwe/spider_tool",
    packages=find_packages(include=['spider_tools', 'spider_tools.*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Framework :: Pytest",
    ],
    install_requires=[
        "requests",
        "lxml",
        "loguru",
        "urllib3",
        "curl_cffi",
        "aiomysql",
        "aiohttp",
        "click",
        "html2text"
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'black',
            'isort',
            'flake8',
            'mypy',
        ],
        'docs': [
            'sphinx',
            'sphinx-rtd-theme',
        ],
    },
    entry_points={
        'console_scripts': [
            'spider-tools-pro=spider_tools.cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        'spider_tools': ['py.typed'],
    },
)