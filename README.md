# Online Banking System

This is a Online Banking Concept created using Django Web Framework.

## Features

* Create Bank Account.
* Load account Details Using Account Number & password.
* Deposit & Withdraw Money.
* Transaction Detail Page.
* Count Monthly Interest Using Celery.

## Prerequisites

Be sure you have the following installed on your development machine:

+ Python >= 3.6.3
+ Redis Server
+ Git 
+ pip
+ Virtualenv (virtualenvwrapper is recommended)

## Requirements

+ celery==4.1.0
+ Django==1.11.20
+ django-celery-beat==1.0.1
+ django-crispy-forms==1.6.1
+ Pillow==4.2.1
+ redis==2.10.6

## Install Redis Server

[Redis Quick Start](https://redis.io/topics/quickstart)

Run Redis server
```bash
redis-server
```

## Project Installation

To setup a local development environment:

Create a virtual environment in which to install Python pip packages. With [virtualenv](https://pypi.python.org/pypi/virtualenv),
```bash
virtualenv venv            # create a virtualenv
source venv/bin/activate   # activate the Python virtualenv 
```

or with [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/),
```bash
mkvirtualenv -p python3 {{project_name}}   # create and activate environment
workon {{project_name}}   # reactivate existing environment
```

Clone GitHub Project,
```bash
git@github.com:saadmk11/banking-system.git

cd banking-system
```

Install development dependencies,
```bash
pip install -r requirements.txt
```

Migrate Database,
```bash
python manage.py migrate
```

Run the web application locally,
```bash
python manage.py runserver # 127.0.0.1:8000
```

Create Superuser,
```bash
python manage.py createsuperuser
```

Run Celery
(Different Terminal Window with Virtual Environment Activated)
```bash
celery -A bankingsystem worker -l info

celery -A bankingsystem beat -l info
```

## Images:
![alt text](https://i.imgur.com/QZwaEHX.png)
#
![alt text](https://i.imgur.com/HTcqWcw.png)
#
![alt text](https://i.imgur.com/HHsmJVD.png)
