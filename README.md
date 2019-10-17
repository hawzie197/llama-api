# pyllama
<a href="https://codeclimate.com/github/hawzie197/pyllama/maintainability"><img src="https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability" /></a>
[![Python 3.6](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Django 2.0](https://img.shields.io/badge/Django-2.0-blue.svg)](https://docs.djangoproject.com/en/2.1/releases/2.0/)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

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