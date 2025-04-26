import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lts-mpsmqutils",
    version="2.1.2",
    description="A set of utilities for communicating with a message queue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.huit.harvard.edu/LTS/mps-mqutils",
    packages=setuptools.find_packages(),
    install_requires=[
        'lts-mpsjobtracker-mongo',
        'requests',
        'pytest',
        'tenacity',
        'cryptography'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        # Include all *.json files in any package
        "": ["*.json"],
    }
)
