from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scoras",
    version="0.3.0",  # Updated version
    author="Anderson L. Amaral",
    author_email="luis.anderson.sp@gmail.com",
    description="Intelligent Agent Framework with Complexity Scoring",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scorastecnologialtda/scoras",
    packages=find_namespace_packages(include=["scoras", "scoras.*"]) ,  # This includes all subpackages
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "httpx>=0.24.0",
        "numpy>=1.20.0",
        "typing-extensions>=4.0.0",
        "asyncio>=3.4.3",
        "aiohttp>=3.8.0",
    ],
) 
