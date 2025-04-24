from setuptools import setup, find_packages

setup(
    name="BacenAPI",
    version="0.3.0",
    author="Paulo Icaro, Lissandro Sousa, Francisco Gildermir",
    author_email="lisandrosousa54@gmail.com",
    description="Package to access time series data from the Central Bank of Brazil via API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LissandroSousa/BacenAPI.py",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "BacenAPI": ["dados/*.txt"], 
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas",
        "requests",
    ],
)