from setuptools import setup, find_packages

setup(
    name="fmpegarm64v8a_mkkk",                      # 包名
    version="0.2.0",                        # 版本号
    author="okfromhere",                     # 作者
    author_email="okfromhere999888@gmail.com ",  # 邮箱
    description="ffmpe on garm64 v8a", # 简短描述
    long_description=open("README.md").read(), # 详细描述
    long_description_content_type="text/markdown",
    url="https://github.com/ffmpegarm64v8a/my_package", # 项目主页
    packages=find_packages(),               # 自动发现包
    install_requires=[                      # 依赖项
        "requests>=2.0.0",
    ],
    classifiers=[                           # 分类标签
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",                # 支持的 Python 版本
)