# setup.py

from setuptools import setup, find_packages

setup(
    name="liberal_alpha",  # PyPI 包名
    version="0.1.8",       # 包版本号
    author="capybaralabs",
    author_email="donny@capybaralabs.xyz",
    description="Liberal Alpha Python SDK for interacting with gRPC-based backend",
    long_description=open("README.md", encoding="utf-8").read(),  # 读取 README.md 作为 PyPI 介绍
    long_description_content_type="text/markdown",
    url="https://github.com/capybaralabs-xyz/Liberal_Alpha",      # 你的仓库地址
    packages=find_packages(exclude=["tests", "tests.*"]),         # 自动查找包，排除测试目录
    include_package_data=True,                                    # 若需要包含非 .py 文件，如 proto/*.proto 等
    install_requires=[
        "grpcio>=1.40.0",
        "protobuf>=3.20.0",
        "requests>=2.20.0",
        "coincurve>=15.0.0",
        "pycryptodome>=3.10.0",
        "eth-account>=0.5.7",
        "eth-keys>=0.3.4",
        "websockets>=8.0.0",
    ],
        entry_points={
        "console_scripts": [
            "liberal_alpha=liberal_alpha.client:main",   # 命令行执行 liberal_alpha 时，会调用 liberal_alpha/client.py 中的 main()
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  
)
