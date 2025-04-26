from pathlib import Path

from setuptools import find_packages, setup

# 读取 README 文件内容
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="aicli-agent",
    version="0.1.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "pydantic-settings",
        "generalagent",
        "rich",
        "tavily-python",
        # 添加其他依赖项
    ],
    entry_points={
        "console_scripts": [
            "aicli=aicli:cli",
        ],
    },
    url="https://github.com/callmexss/aicli",  # 项目主页
    project_urls={
        "PyPI": "https://pypi.org/project/aicli-agent/",  # PyPI 链接
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
