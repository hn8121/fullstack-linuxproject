# fullstack-linuxproject
###########################################################
# File: README.md
# Author: Howard Nathanson
#         Full Stack Nanodegree - project 3 - Linux Server
# History: 09/15/2019 - Initial Version


Overview:
The program will produce a simple sport league website containing teams which can be run via a URL on any browser. The site is run on an Ubuntu server hosted Amanzon Web Services (AWS) Lightsail and uses Google and Facebook APIs for login functionality. The website is running in a virtual environment and is written in Python, HTML, Flask, and Linux. It is running on an apache2 server using wsgi. The data is stored in a PostgreSQL database.

The code is stored in this Git repository. The code is ogranized in folders:
	* catalog (current folder) - containing the web and database code files
	* static - folder containing the css and graphic files
	* templates - folder containing the flask html template files
	* venv - folder containing the virtual enviroment files

NOTE: The AWS, Google API, and Facebook API accounts were closed upon confirmation of the completion of this nanodegree. The details below are provided as required by this project.

Website Configuration:
The Ubuntu Linux server is hosted on AWS Lightsail. AWS Lightsail can be found at https://lightsail.aws.amazon.com/ls/webapp. The URL for the assigned IP Address can be found by a reverse lookup. I used https://mxtoolbox.com/ReverseLookup.aspx.
* Statuc IP Address: 3.225.25.4
* URL: http://ec2-3-225-25-4.compute-1.amazonaws.com/

On your local server, create the public key to allow password-less logins to the Ubuntu server
* run: ssh-keygen
	(provide a <directory>/<filename> to save the keys. For this project, the <filename> is grader)
The <directory>/grader.pub file contains the public key. This key will be copied into a file on the Ubuntu server in the next set of steps.

On the server, create the "grader" user id with appropriate permissions
* run: sudo add user grader (creates the grader user id)
* run: sudo vi /etc/sudoers.d/grader (new file)
	Add the following comment and permission line to the file
	* # User rules for ubuntu
	  grader ALL=(ALL) NOPASSWD:ALL

Create the authorized keys file on the Ubuntu server to allow password-less entry
* Login as grader on the Ubuntu server
* run: mkdir .ssh
* run: vi .ssh/authorized_keys
	copy the contents of the <directory>/grader.pub into .ssh/authorized_keys
* run: chmod 700 .ssh (restrict access to directory to grader id)
* run: chmod 644 .ssh/authorized_keys (only allow grader to update the file)

CONFIGURE THE SECUTIRY ON THE SERVER
* run: sudo vi /etc/ssh/sshd_config (edit the ssh configurations)
	* udpate the line "PasswordAuthentication yes" to PasswordAuthentication no" (disable login by password)
	* update the line "PermitRootLogin prohibit-password" to "PermitRootLogin no" (disable root login)
	* add the line "AllowUsers grader" (can login via the grader user id)
* save the file and exit.
* run: sudo service ssh restart (restart the server with the updated configurations)

CONFIGURE THE FIREWALLS
* run: sudo ufw default deny incoming (default deny all incoming traffic)
* run: sudo ufw default allow outgoing (default allow all outgoing traffic)
* run: sudo ufw deny 22 (deny traffic on port 22) 
* run: sudo ufw allow 2200/tcp (allow traffic on port 2200)
* run: sudo ufw allow www (allow http traffic on its default port 80)
* run: sudo ufw allow 123/udp (allow udp traffic on port 123)
* run: sudo ufw enable (apply the updates)
* run: sudo ufw status (confirm the settings)
Here is my status:

Status: active
To                         Action      From
--                         ------      ----
2200/tcp                   ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
123/udp                    ALLOW       Anywhere
123                        ALLOW       Anywhere
2200/tcp (v6)              ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
123/udp (v6)               ALLOW       Anywhere (v6)
123 (v6)                   ALLOW       Anywhere (v6)

CONFIGURE THE SERVER AND INSTALL THE REQUIRED PACKAGE

NOTE: Packages are installed for Python3. Also, the installs can be combined instead of one per line.
* run: sudo dpkg-reconfigure tzdata (change the timezone, select UTC in the dropdown)
* run: sudo apt-get install apache2 
* run: sudo apt-get install libapache2-mod-wsgi-py3
* run: sudo apt-get install python-dev
* run: sudo apt-get install python3-pip 
* run: sudo apt-get install postgresql (install database)
* run: sudo apt-get install python3-psycopg2
* run: sudo apt-get install git
* run: sudo pip install virtualenv (install virtual environment)
* run: sudo pip install Flask 
* run: sudo pip install SQLAlchemy
* run: sudo pip install oathlib
* run: sudo pip install oath2client

To verify what is installed, run sudo pip list

CREATE A CONFIG FILE FOR THE PROJECT

* run: sudo cp /etc/apache2/sites-enabled/000-default.conf /etc/apache2/sites-enabled/catalog.conf
* run: sudo vi /etc/apache2/sites-enabled/catalog.conf (edit file for project)
	Add the following contents to the file (specific to this project):
<VirtualHost *:80>
        ServerName 3.225.25.4
        ServerAdmin admin@3.225.25.4
        ServerAlias ec2-3-225-25-4.compute-1.amazonaws.com
        
        WSGIScriptAlias / /var/www/catalog/catalog/catalog.wsgi

        <Directory /var/www/catalog/catalog/>
                Order allow,deny
                Allow from all
        </Directory>

        Alias /static /var/www/catalog/catalog/static
        <Directory /var/www/catalog/catalog/static/>
                Order allow,deny
                Allow from all
        </Directory>

        LogLevel warn
        ErrorLog ${APACHE_LOG_DIR}/catalogerror.log
        CustomLog ${APACHE_LOG_DIR}/catalogaccess.log combined
</VirtualHost>

	Save the file and exit

* run: sudo a2edissite 000-default.conf (disable the default config file)
* run: sudo a2ensite catalog.conf (enable the new catalog config file)
* run: sudo service apache2 reload (load all the updates and other packages)
* run: sudo service apache2 restart (apply the updates)
* run: sudo virtual venv (creates the environment for a virtual server)
* run: sudo venv/bin/activate (activates the virtual envorinment)

IMPORT THE CODE AND UPDATE CODE FILES TO RUN FROM THE UBUNTU SERVER
* run: sudo mkdir /var/www/catalog 

Since my GitHub repository contains all the files from all the projects, I imported them to a temporary directory and then copied the catalog folder into the project area.
* run: sudo mkdir /var/www/git (temp folder)
* run: cd /var/www/git
* run: git clone https://github.com/hn8121/fullstack-nanodegree-vm.git full-stack-nanodegre-vm
* run: cp -R full-stack-nanodegree-vm/vagrant/catalog ../catalog/.  (recursive copy of the catalog files)
* run: cd /var/www/catalog/catalog

Create the home wsgi file
* run: sudo vi catalog.wsgi
	Enter the following contents:
#!/usr/bin/env python3
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/catalog/catalog/")
from __init__ import app as application
application.secret_key = 'please_work_for_me'

Save and exit the file.

* run: sudo mv catalog_project.py __init__.py (this is the file defined in catalog.wsgi to contain the website code)
* run: sudo vi __init__.py
	replace the database connection line for sqlite to postgresql
	delete the line with: engine = create_engine('sqlite:///catalog.db)
	add the line: engine = create_engine('postgresql://catalog:<password>@localhost/catalog')
Save and exit the file.

ENABLE OAUTH LOGIN

Update the credentials on the Google developers console website (https://console.developers.google.com) to allow it to recognize the project server.

On the OAuth consent screen page, add the authorized domains for the project and save
	* amanzonaws.com
	* xip.io
On the Credentials page, select the link for the current project name and add to the Authorized Javascript origins and save
	* http://ec2-3-225-25-4.compute-1.amazonaws.com (my URL)
	* http://3.225.25.4/xip.io (my IP address)
On the Credentials page, select the link for the current project name and add to the Authorized redirect URIs and save
	* http://ec2-3-225-25-4.compute-1.amazonaws.com/login
	* http://ec2-3-225-25-4.compute-1.amazonaws.com/gconnect
	* http://3.225.25.4.xip.io/login
	* http://3.225.25.4.xip.io/gconnect

On the Credentials page, click the DOWNLOAD JSON link

On the Ubuntu server, copy the contents of the downloaded file into the /var/www/catalog/catalog/client_secrets.json file

Since the virtual server must have the full directory path to know where to find files, the references to the client_secrets.json and facebook_secrets.json files must be updated.
*run: sudo vi __init__.py
	replace every reference to client_secrets.json with /var/www/catalog/catalog/client_secrets.json
	replace every reference to fb_client_secrets.json with /var/www/catalog/catalog/fb_client_secrets.json
Save and exit the file.

CREATE AND POPULATE THE DATABASE

Run the following sequence from the Ubuntu server, from the /var/www/catalog/catalog directory where the database files reside

* run: sudo -i -u postgres (become id postgres, the default database superuser)
* run: psql (connect to the database)
* run: CREATE ROLE catalog WITH PASSWORD <password>; (creates the catalog db user id)
* run: CREATE DATABASE catalog WITH ALLOW_CONNECTIONS false; (creates the catalog database but denies remote connections) 
* run: \c catalog (connect to database catalog)
* run: REVOKE ALL ON SCHEMA public FROM public; 
* run: GRANT ALL ON SCHEMA public TO catalog;   (with previous line, restrict database access)
Exit the database and logout of postgres id

* run: psql -d catalog -f catalog_db_setup.sql (create the database tables)
* (optional) run: psql -d catalog -f catalog_db_starterdata.sql (populates sample data into the tables). This allows multiple owners to be created since updates are based on owner. 

* run: sudo service postgresql restart (bounce the database)

RUN THE WEBSITE

From any broswer, enter the website using either the IP address or the URL

http://3.225.25.4/
http://ec2-3-225-25-4.compute-1.amazonaws.com/

NOTE: The website will only work until the nanodegree is completed, then the IP address will be disabled. 


