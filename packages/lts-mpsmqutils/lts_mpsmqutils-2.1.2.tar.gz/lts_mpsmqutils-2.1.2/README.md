# mps-mqutils

## Introduction
A set of utilities for Media Preservation Services that provides standard methods to communicate with the message queue.

## Prerequisites
Read the README in the worker prototype project [mps-worker-prototype](https://github.huit.harvard.edu/LTS/mps-worker-prototype/blob/main/README.md) for information on how to build and integrate a worker microservice. Read the [WORKER PROGRAMMING](https://github.huit.harvard.edu/LTS/mps-worker-prototype/blob/main/README.md#worker-programming) section for the standard worker API request and responses that are required.

Example worker API responses

Task was successful:

```
{ success: 'true' }
```

Task did not complete successfully:
```
{ success: 'false', 'error': 'Example error', 'message': 'Example error message' }
```

## Technology Stack
##### Language
Python

##### Development Operations
Docker Compose

## Configuration
This package reads configuration values from environment variables.

## Installation

```
$ pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ lts-mpsmqutils
$ python
>>> from mpsmqutils import mqlistener, mqutils
>>> mqutils.__create_message('0922a78fd89f_2a5ff037-462a-4642-8bd0-7546d7580e1a', 1, 'success')
```

## Local Development Environment Setup Instructions

### 1: Clone the repository to a local directory
git clone git@github.huit.harvard.edu:LTS/mps-mqutils.git

### 2: Create app config

##### Create config file for environment variables
- Make a copy of the config example file `./env-example.txt`
- Rename the file to `.env`
- Replace placeholder values as necessary

*Note: The config file .env is specifically excluded in .gitignore and .dockerignore, since it contains credentials it should NOT ever be committed to any repository.*

### 3: Start

##### START

To build the image without the cache, run the build command with the --no-cache option. The no cache option is required when updating any dependencies.

```
docker-compose -f docker-compose-local.yml build --no-cache && docker-compose -f docker-compose-local.yml up -d --force-recreate
```

### 4: Open a shell in the container

##### Run docker exec to execute a shell in the container by name

Open a shell using the exec command to access the mps-mqutils container.

```
docker exec -it mps-mqutils bash
```

### 5: Install dependencies
This step is only required if additional python dependencies must be installed. Update the requirements.txt inside the container to install new python packages in the project. If the dependencies are required for the package to run, they also must be included in the `install_requires` section of setup.py.

##### Install a new pip package

Once inside the mps-mqutils container, run the pip install command to install a new package and update the requirements text file.

```
pip install packagename && pip freeze > requirements.txt
```

##### Add dependencies to setup

Add the names of the dependencies to the `install_requires` section of setup.py. Read more about adding dependencies in this article [Specifying dependencies](https://python-packaging.readthedocs.io/en/latest/dependencies.html).

### 6: Build and publish the package

#### Step 6A: Prepare the distribution
* Update the version number in `setup.py`
* To publish a pre-release version, add a letter and a number after the version number e.g. `0.0.1a1`
* Remove the old `dist/` directory from the previous build if necessary

#### Step 6B: Build the distribution

Once inside the container, build the distribution.

`python3 setup.py sdist bdist_wheel`

A new directory `dist` will be created in the container.

#### Step 6C: Register for an account

[Register for an account](https://test.pypi.org/account/register/) on the test python package repository. Enable two-factor authentication for logins. [Create a token](https://test.pypi.org/manage/account/#api-tokens).

#### Step 6D: Upload package to the test repository

Publish the package to the test repository `testpypi` before publishing it to the production repository.

`python3 -m twine upload --repository testpypi dist/*`

#### Step 6E: Test the package
Open the package in the repository and view the version history.

https://test.pypi.org/project/lts-mpsmqutils/0.0.1/

Read [Installation](#installation) in this document for instructions on how to install and test the package in another project or environment.

### 7: Stop

##### STOP AND REMOVE

This command stops and removes all containers specified in the docker-compose-local.yml configuration. This command can be used in place of the 'stop' and 'rm' commands.

```
docker-compose -f docker-compose-local.yml down
```

## More information
Read the documenation for more information on building and publishing the distribution.

* [Generating distribution archives](https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives)

* [Uploading the distribution archives](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives)

* https://tom-christie.github.io/articles/pypi/