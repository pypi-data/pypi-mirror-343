from setuptools import setup, find_packages

setup(
    name="virtuered-webui",
    version="0.1.1",
    author="Yijia Zheng",
    author_email="yijiazheng17@gmail.com",
    description="VirtueRed Web UI packaged with Python CLI",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/virtuered-webui",  # optional
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "click",
        "pyfiglet",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "virtuered-webui=virtuered_webui.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
