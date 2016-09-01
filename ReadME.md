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
There are two commands to ensure that data is synced.

To download:

`python malariatool/manage.py dhis2_data_download 201502`

To parse:

`python malariatool/manage.py dhis2_data_parse 201502`

The above commands should be setup to run as cron jobs late in the night. 

####DEPLOYMENT

The deployment process is based on a free software platform called Ansible which enables one to provision multiple servers with just a single command.

The Ansible software is not supported on the Windows platform even though certain people have managed to get it running on Cygwin.

**Installing Ansible onto a Ubuntu machine**

`$ sudo apt-get update`

`$ sudo apt-get install software-properties-common`

`$ sudo apt-add-repository ppa:ansible/ansible`

`$ sudo apt-get update`

`$ sudo apt-get install ansible`

**Cloning the Malaria Tool repository**

`$ sudo apt-get install git`

`$ git clone https://github.com/CHAIUganda/MalariaTool.git`

`$ cd ~/MalariaTool/provision`

**Update the hosts configuration file (inventory/hosts.ini)**

`x.x.x.x ansible_ssh_user=ubuntu ansible_ssh_private_key_file=~/key.pem`

**Update the vars configuration file (vars.yml)**

Set the secret to the database password e.g. postgres

**Run deployment**

`$ ansible-playbook app_server.yml -i inventory/hosts.ini -vvvv`

**Wrapping up**

Rename the local_settings.py.sample file to local_settings.py in the provisioned instance and make changes to it accordingly.



The frontend is written in BoostrapCSS, JQuery with a few plugins and LeafLetJs for the maps section.


