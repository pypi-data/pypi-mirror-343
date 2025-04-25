from setuptools import setup, find_packages

setup(
    name="fastapi-websocket-validation",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.115.0",
        "pydantic>=2.0.0",
    ],
    author="Dhiraj Bomma",
    author_email="dhirajbomma@gmail.com",
    description="A FastAPI WebSocket message validation and handling library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zyx-db/fastapi-websocket-validation",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
) 