from setuptools import setup, find_packages

setup(
    name="signalwire-swml",
    version="1.24",
    author="Brian West",
    author_email="brian@signalwire.com",
    description="A Python package for generating SignalWire Markup Language (SWML)",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/briankwest/signalwire-swml",
    packages=find_packages(),
    license="MIT",
    include_package_data=True,
    install_requires=[
        "pyyaml>=5.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8"

) 