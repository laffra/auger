import setuptools

setuptools.setup(
    name="auger-python",
    version="0.1.29",
    author="Chris Laffra",
    author_email="laffra@gmail.com",
    description="Automatically generate unit tests for Python code",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/laffra/auger",
    packages=[
        'auger',
        'auger.generator'
    ],
    install_requires=[
        'funcsigs',
        'mock',
        'six',
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ])
