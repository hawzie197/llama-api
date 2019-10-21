# pyllama
[![Build Status](https://travis-ci.org/hawzie197/llama-api.svg?branch=master)](https://travis-ci.org/hawzie197/llama-api)
[![codecov](https://codecov.io/gh/hawzie197/llama-api/branch/master/graph/badge.svg)](https://codecov.io/gh/hawzie197/llama-api)
[![Maintainability](https://api.codeclimate.com/v1/badges/d05a1c8f7fee0c3e0b04/maintainability)](https://codeclimate.com/github/hawzie197/llama-api/maintainability)
[![Known Vulnerabilities](https://dev.snyk.io/test/github/hawzie197/llama-api/badge.svg)](https://dev.snyk.io/test/github/hawzie197/llama-api)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Django 2.0](https://img.shields.io/badge/Django-2.0-blue.svg)](https://docs.djangoproject.com/en/2.1/releases/2.0/)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![flake8](https://img.shields.io/badge/linter-flake8-lightgrey)](https://img.shields.io/badge/linter-flake8-lightgrey)

## Overview
pyllama automatically summarizes main points in the privacy policies whenever a user visits a signup page of a website. On page load, the pyllama searches for its privacy policy. If found, the extension parses the privacy policy using Natural Language Processing, and then displays 'what the website collects', 'why it collects that information', and whether or not the site adhears to gdpr allowing its user to delete personal data points off the company's servers for good.
If no policy is found, or a low confidence interval is returned, a warning is displayed to the user.


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

### Example Case
```bash
http://localhost:8000/api/analyze/?url=https://www.nytimes.com/
```
