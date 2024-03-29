<p align="center">
    <img src="assets/QuickCheckLogo.svg"
        height="50">
</p>

---


<a href="https://www.djangoproject.com/" alt="Flutter"><img src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray" /></a> 
<a href="https://github.com/tonydoesathing/quickcheck-backend/releases" alt="Figma"><img src="https://img.shields.io/github/v/release/tonydoesathing/quickcheck-backend" /></a>
<a href="https://github.com/tonydoesathing/quickcheck-backend" alt="Figma"><img src="https://img.shields.io/github/last-commit/tonydoesathing/quickcheck-backend" /></a> 

[QuickCheck](https://github.com/tonydoesathing/quickcheck) is a cross-platform application for teachers that assists in rapid formative assessment so they can focus more on teaching and less on organization. This project provides the networked synchronization required to run [QuickCheck](https://github.com/tonydoesathing/quickcheck).

## Setup
Set the `DJANGO_SECRET_KEY` and `DJANGO_DEBUG` environment variables, with a secure secret key (preferably randomly generated) and `True`/`False` respectively.

Ensure that you're using Python3.

Run `python -m venv .env` in the source directory, and then `.env/Scripts/activate`, `python -m pip install -r requirements.txt`, and `python manage.py migrate`, in that order. It should create the database.

To set up on a Google Cloud Server, see the example at the end of this README.

## Running
Simply run `python ./manage.py runserver`

## Generating UML diagram
Run `python manage.py graph_models -a -g --dot -o quickcheck-backend.dot`; this will export a GraphViz .dot file.
Ensure that you have GraphViz enabled.
Run `dot.exe -Tpng quickcheck-backend.dot -o quickcheck-backend-uml.png`

## Authentication
Admin users can be added via 'python manage.py createsuperuser'.
Further users can be added by logging into `{server-ip}/admin` and adding them in the "Users" section.
A token can be retrieved by the /auth/api-token-auth/ endpoint (see postman collection).
Token must be put in the "Authorization" field in the http header following the `Token {token}` convention.

## Endpoints Documentation

Most requests require an auth header which takes 'Authorization' as a key and 'Token {token}' as the value. '{token}' is retrieved using the 'auth/api-token-auth' endpoint as documented below (this is the only endpoint that doesn't need an auth header).  

### Students

'/api/students/{student_id}'

#### GET

Gets a student by ID. If '{student_id}' is left blank then the endpoint returns all students that belong to the currently authenticated user. 

#### DELETE

Deletes student by ID.

#### POST

Adds a student. Does not take a student ID, as one is created automatically and returned with the response.

Example request body format:
'''
{
    "name": "Bob",
    "groups": [1, 3],
    "class_id": 5
}
'''

#### PUT

Edit student by ID. Body should be formatted in the same way as the POST method, but with the new values. 

### Groups

'/api/groups/{group_id}'

#### GET

Gets a group by ID. Use the '?class_id={id}' argument in the place of '{group_id}' to get all groups in a given class.

#### DELETE

Deletes group by ID

#### POST

Creates a group. Does not take a group ID, as one is created automatically and returned with the response.

Example request body format:
'''
{
    "name": "Group 1",
    "student_set": [1,2,3],
    "class_id": 2
}
'''

#### PUT

Edit group by ID. Body should be formatted in the same way as the POST method, but with the new values. 

### Assessments

'/api/assessments/{assessment_id}'

#### GET

Gets an assessment by ID. Use the '?class_id={id}' argument in the place of '{assessment_id}' to get all assessments in a given class.

#### DELETE

Deletes assessment by ID

#### POST

Creates an assessment. Does not take an assessment ID, as one is created automatically and returned with the response.

Example request body format:
'''
{
    "name": "Assessment 1",
    "class_id": 5,
    "student_scores": [
        {
            "student_id": 1,
            "score": 2
        }
    ],
    "group_scores": [
        {
            "group_id": 1,
            "score": 2
        }
    ]
}
'''

#### PUT

Edit assessment by ID. Body should be formatted in the same way as the POST method, but with the new values. 

### Classes

'/api/classes/{class_id}'

#### GET

Gets an class by ID. Leave '{class_id}' blank to get all classes that belong to the current user.

#### DELETE

Deletes class by ID

#### POST

Creates a class. Does not take a class ID, as one is created automatically and returned with the response.

Example request body format:
'''
{
    "name": "Class 1"
}
'''

#### PUT

Edit class by ID. Body should be formatted in the same way as the POST method, but with the new values. 

### Authentication

All authentication related endpoints use the post method.

Use the '/auth/api-token-auth/' endpoint to get an auth token. No auth header is necessary for this.

Example request body format:
'''
{
    "username": "admin",
    "password": "password123"
}
'''

Use the '/auth/logout/' endpoint to remove the current token from the backend so it can no longer be used. No body is necessary.

Use the '/auth/logoutall/' endpoint to remove all tokens belonging to the current user so they can no longer be used. No body is necessary.






## Google Cloud Setup
If on Google Cloud Compute Engine follow instructions to create an apache server: [basic webserver with Apache](https://cloud.google.com/compute/docs/tutorials/basic-webserver-apache)



### Install necessary packages:
```
sudo apt update && sudo apt -y install apache2
sudo apt-get update
sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
sudo pip3 install virtualenv
```

### Set up quickcheck backend:
```
git clone https://github.com/tonydoesathing/quickcheck-backend.git quickcheck_backend
cd quickcheck_backend
virtualenv env
. env/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
```

Set the `DJANGO_SECRET_KEY` environment variable to the output of
`python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'`

Set the `DJANGO_DEBUG` environment variable to `False`

One can set the environment variables by modifying the virtualenv script and at `/etc/apache2/envvars`

### Configure apache to connect to django:
`sudo nano /etc/apache2/apache2.conf`

Paste at end:
```
# Quickcheck configurations
WSGIScriptAlias / /home/quickcheckapp/quickcheck_backend/quickcheck/wsgi.py
WSGIPythonHome /home/quickcheckapp/quickcheck_backend/env
WSGIPythonPath /home/quickcheckapp/quickcheck_backend
WSGIPassAuthorization On

<Directory /home/quickcheckapp/quickcheck_backend/quickcheck>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
```

Save (ctrl + x)

Add allowed host:
```
sudo nano quickcheck/settings.py
```

Set:
```
ALLOWED_HOSTS = [address]
```

### Update firewall permissions:
```
sudo ufw allow 'Apache Full'
sudo chmod 664 /home/<user>/quickcheck_backend/db.sqlite3
sudo chown :www-data /home/<user>/quickcheck_backend/db.sqlite3
sudo chown :www-data /home/<user>/quickcheck_backend
```

### Enable https with [certbot](https://certbot.eff.org/instructions?ws=apache&os=ubuntufocal)

Make sure snapd is installed

Update snapd:
```
sudo snap install core; sudo snap refresh core
```

Make sure already installed certbot is removed

Install certbot:
```
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

Run certbot:
```
sudo certbot --apache
```

Test auto renew
```
sudo certbot renew --dry-run
```

Restart apache:
```
sudo service apache2 restart
```

### To update:
```
cd quickcheck_backend
git pull

python -m pip install -r requirements.txt
python manage.py migrate
sudo service apache2 restart
```
