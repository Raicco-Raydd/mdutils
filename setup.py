from setuptools import setup, find_packages

setup(
    name="mdutils",
    version="2.3.1",
    description="Markdown 文档工具箱 — 为Openclaw Agent提供的Markdown文档处理工具，可便捷强化openclaw对于Markdown文档的处理能力。",
    packages=find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    author="Raicco&Raydd",
    email="chen.antrand@qq.com",
    entry_points={
        "console_scripts": [
            "mdutils=mdutils.cli:main",
        ],
    },
)
