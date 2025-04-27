from setuptools import setup, find_packages

setup(
    name="macroscopic_recall",          # 包名（PyPI唯一）
    version="0.1.0",            # 版本号（遵循语义化版本）
    author="yanpei.fan",
    author_email="yanpei.fan@centurygame.com",
    description="宏观召回系统组件",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/my_package",
    packages=find_packages(),
    install_requires=[          # 依赖项
        "openai~=1.73.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",    # Python版本要求
)
