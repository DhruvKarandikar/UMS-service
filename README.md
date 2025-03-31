About User Management Project:

The User Management System developed using Django and Django REST Framework is a comprehensive solution designed to streamline user-related operations within an organization. This project facilitates efficient management of user profiles,user referrences offering a user login, signup interactions. This system allows for the creation, retrieval, updating, and deletion of user profiles, each identified by a unique refer code. Through a RESTful API design, this project ensures seamless integration with other systems and applications, promoting interoperability and ease of use. Token-based authentication secures API endpoints, safeguarding sensitive user's information.

Setting Up the project in you Local System:

Firstly, Use git clone and copy the project ssh into your terminal 

-  command - python3 -m venv {your env file name} // for creating the python env file for the project
-  command - .\env\Scripts\activate // to activate the evironment and then it will make the libraries install within the env
-  command - pip install -r requirements.txt

For Databases connections Postgres is used as the Engine Kindly, create the Database in Postgres

Hardcode the given values in the settings.py file

DATABASES = { 'default': { 'ENGINE': 'django.db.backends.postgresql', 'NAME': os.environ.get("POSTGRES_NAME"),
'USER': os.environ.get("POSTGRES_USER"), 'PASSWORD': os.environ.get("POSTGRES_PASSWORD"), 'HOST': os.environ.get("POSTGRES_HOST"), 'PORT': '5432', 'ATOMIC_REQUESTS': True, } }

A postgresql needs to be install by default pgadmin 16.0 to interact with the Database

An .env file needs to be created in order to interact with the postgresql database:
an .env file will look like this in key value pairs
-  POSTGRES_NAME={postgres database name}
-  POSTGRES_USER={postgres username}
-  POSTGRES_PASSWORD={postgres password}
-  POSTGRES_HOST={postgres hostname} // incase it is local device user "localHost"
-  DJANGO_SECRET_KEY={you django secret} // 
-  DJANGO_DEBUG="true" // false when it is on production


Making a database schema in your local system

Command - python manage.py migrate 
Command - python manage.py runserver

After going to the localhost server in default browser Swagger Settings are made in the API to make API interactive with UI UX 

Features:
- Custom Middleware
- Generic API's
- Jwt Authentication
- Override Django Methods
- Reduced API vulnerability
- Interactive API's using Swagger
- Whitenoise and production ready environment 
