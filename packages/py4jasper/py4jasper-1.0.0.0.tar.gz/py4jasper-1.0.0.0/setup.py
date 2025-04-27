from setuptools import setup, find_packages

setup(
    name="py4jasper",
    version="1.0.0.0",
    description="Python package for generating reports using Jasper",
    long_description=open('README.md').read(),  # ? Reads the content of your README file
    long_description_content_type="text/markdown",
    author="Sanskar Gandhi",
    author_email="sanskargandhi2000@gmail.com",
    packages=find_packages(),
    install_requires=["py4j"],  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
