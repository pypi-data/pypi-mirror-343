from setuptools import setup, find_packages

# 安全读取 README.md
with open("unisound_agent_frame/README.md", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="unisound-agent-frame",          # 包名（pip install时用）
    version="0.0.1",              # 版本号
    author="unisound",
    author_email="your.email@example.com",
    description=long_description,
    long_description="unisound-agent-frame",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my-framework",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "unisound_agent_frame": [
            "scripts/*",
            "template/*",
            "*.md",
            ".gitignore",
            "LICENSE",
        ]
    },
    entry_points={
        'console_scripts': [
            'unisound-agent-frame-init=unisound_agent_frame.cli:init',  # 定义初始化命令
        ],
    },
    install_requires=[           # 依赖项
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "sqlalchemy>=1.4.0",
        "aiofiles>=0.8.0",
        "aioredis>=2.0.0",
        "pyyaml>=6.0",
        "python-multipart>=0.0.5",
        "aiomysql>=0.1.1",
        "aiohttp>=3.8.0",
        "loguru>=0.6.0",
        "starlette>=0.21.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="MIT",  # 使用 SPDX 许可证标识符
    license_files=("unisound_agent_frame/LICENSE",),  # 指定 LICENSE 文件位置
    python_requires=">=3.5",     # Python版本要求
)