from setuptools import setup, find_packages
import os

readme_path = "readme.md"

with open(readme_path, "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pythonweblog_client_ws",
    version="0.7.0",
    author="Lucas Bueno",
    author_email="asuma312@gmail.com",
    description="Python client for the pythonweblog",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asuma312/python-weblogging",
    packages=['pyweblog','pyweblog/SDK_WS'],
    package_data={
        'pyweblog': ['readme.md'],
    },
    keywords='pythonweblog, python, client, websocket, logging, log, logger',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "python-socketio",
        "websocket-client"
    ],
)