# pyllama
[![Build Status](https://travis-ci.com/hawzie197/pyllama.svg?branch=master)](https://travis-ci.com/hawzie197/pyllama)
[![codecov](https://codecov.io/gh/hawzie197/pyllama/branch/master/graph/badge.svg)](https://codecov.io/gh/hawzie197/pyllama)
<a href="https://codeclimate.com/github/hawzie197/pyllama/maintainability"><img src="https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability" /></a>
[![Python 3.6](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Django 2.0](https://img.shields.io/badge/Django-2.0-blue.svg)](https://docs.djangoproject.com/en/2.1/releases/2.0/)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![flake8](https://img.shields.io/badge/linter-flake8-lightgrey)](https://img.shields.io/badge/linter-flake8-lightgrey)

## Overview
A guard based chrome extension that lets you know if a company allows deletion of your data before you signup, based on their privacy policy.


### Quick Setup

First, download docker desktop from [here](https://www.docker.com/products/docker-desktop).
```bash
git clone https://github.com/hawzie197/pyllama.git
cd /pyllama

docker-compose up --build
```
navigate to http://localhost:8000

**Registered API Urls**
```text
/api/accounts/users/
/api/accounts/groups/
```

### Linting (Flake8)
Follow [this](https://gist.github.com/tossmilestone/23139d870841a3d5cba2aea28da1a895) to setup flake8 with pycharm


### Code Formatting (Black)
Follow [this](https://github.com/psf/black), ctrl-f for `Optionally, run Black on every file save`

### Testing (unittest)
```bash
docker-compose run django ./manage.py test
```