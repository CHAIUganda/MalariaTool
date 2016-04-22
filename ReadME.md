##Malaria Tool

This tool is written the following techstack.

- Python 2.7
- Django 1.8.3
- Postgres


####Installation:
Ensure Python 2.7.x, `pip` and `virtualenv` installed. 

Because its a python/django project is advised to run in separate virtual environment using either virtualenv by installing it via `pip install virtualenv` and creating one `virtualenv malariatool` 

####Installing of requirements.
Activate the virtualenv `source malariatool/bin/activate`
then install python requirements using pip `pip install -r requirements.txt `   

####To runserver:

`python malariatool/manage.py runserver`

####To run test:

`python malariatool/manage.py test`

####User Management:
There are three user roles AdminRole, IPUserRole and Public Users.

To create a admin user:

`python malariatool/manage.py createsuperuser`

And use that to login and create other users.

####Data Management:
There are too commands to ensure that data is synced.

To download:

`python malariatool/manage.py dhis2_data_download 201502`

To parse:

`python malariatool/manage.py dhis2_data_parse 201502`

The above commands should be setup to run as cron jobs late in the night. 

The frontend is written in BoostrapCSS, JQuery with a few plugins and LeafLetJs for the maps section.


