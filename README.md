<br>
<p align="center">
  <img alt="HackCU" src="https://github.com/HackCU/splash-page/blob/master/img/hackcu_black.png" width="200"/>
</p>
<br>


[![Maintainability](https://api.codeclimate.com/v1/badges/0806a9c40ea11ded0efd/maintainability)](https://codeclimate.com/github/HackCU/backend/maintainability)
[![Build Status](https://travis-ci.org/HackCU/backend.svg?branch=master)](https://travis-ci.org/hackcu/backend)

Backend for hackathon application management. Forked and adapted from [HackUPC's Backend](https://github.com/hackupc/backend).

## Features

- Email sign up
- Email verification
- Forgot password
- Hackathon registration
- Internal user role management: Hacker, Organizer, Volunteer, Director and Admin
- Review applications interface for organizers (includes vote)
- Automatic control of confirmation, expiration and cancellation flows
- Check-in interface with QR scanner
- Django Admin dashboard to manually edit applications, reimbursement and users
- Flexible email backend (SendGrid is the default and recommended supported backend)
- Reimbursement management interface
- (Optional) Automated slack invites on confirm 



## Setup

Needs: Python 3.X, virtualenv

- `git clone https://github.com/hackcu/backend && cd backend`
- `virtualenv env --python=python3`
- `source ./env/bin/activate`
- `pip install -r requirements.txt`
- (Optional) If using Postgres, set up the necessary environment variables for its usage before this step
- `python manage.py migrate`
- `python manage.py createsuperuser` (creates super user to manage all the app)

## Available enviroment variables

- **SG_KEY**: SendGrid API Key. Mandatory if you want to use SendGrid as your email backend. You can manage them [here](https://app.sendgrid.com/settings/api_keys).  Note that if you don't add it the system will write all emails in the filesystem for preview.
You can replace the email backend easily. See more [here](https://djangopackages.org/grids/g/email/). Also enables Sendgrid lists integration.
- **PROD_MODE**(optional): Disables Django debug mode. 
- **SECRET**(optional): Sets web application secret. You can generate a random secret with python running: `os.urandom(24)`
- **PG_PWD**(optional): Postgres password. Also enables Postgres as the default database with the default values specified below.
- **PG_NAME**(optional): Postgres database name. Default: backend
- **PG_USER**(optional): Postgres user. Default: backenduser
- **PG_HOST**(optional): Postgres host. Default: localhost
- **DOMAIN**(optional): Domain where app will be running. Default: localhost:8000
- **SL_TOKEN**(optional): Slack token to invite hackers automatically on confirmation. You can obtain it [here](https://api.slack.com/custom-integrations/legacy-tokens)
- **SL_TEAM**(optional): Slack team name (xxx on xxx.slack.com)


## Server

### Local environment

- Set up (see above)
- `python manage.py runserver`
- Sit back, relax and enjoy. That's it!

### Production environment

Inspired on this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04) to understand and set it up as in our server.

- Set up (see above)
- - `pip install -r requirements/prod.txt`
- Create server.sh from template: `cp server.sh.template server.sh`
- `chmod +x server.sh`
- Edit variables to match your environment and add extra if required (see environment variables available above)
- Create restart.sh from template: `cp restart.sh.template restart.sh`
- `chmod +x restart.sh`
- Edit variables to match your environment and add extra if required (see environment variables available above)
- Run `restart.sh`. This will update the database, dependecies and static files.
- Set up Systemd (read next section)

#### Set up gunicorn service in Systemd
Needs: Systemd.

- Edit this file `/etc/systemd/system/backend.service`
- Add this content
```
[Unit]
Description=backend daemon
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/project_folder
ExecStart=/home/user/project_folder/server.sh >>/home/user/project_folder/out.log 2>>/home/user/project_folder/error.log

[Install]
WantedBy=multi-user.target

```

- Replace `user` for your linux user.
- Replace `project_folder` by the name of the folder where the project is located
- Create and enable service: `sudo systemctl start backend && sudo systemctl enable backend`


#### Set up Postgres

Needs: PostgreSQL installed

- Enter PSQL console: `sudo -u postgres psql`
- Create database: `CREATE DATABASE backend;`
- Create user for database: `CREATE USER backenduser WITH PASSWORD 'password';` (make sure to include a strong password)
- Prepare user for Django

```sql
ALTER ROLE backenduser SET client_encoding TO 'utf8';
ALTER ROLE backenduser SET default_transaction_isolation TO 'read committed';
ALTER ROLE backenduser SET timezone TO 'UTC';
```

- Grant all priviledges to your user for the created database: `GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;`
- Exit PSQL console: `\q`

Other SQL engines may be used, we recommend PostgreSQL for it's robustness. To use other please check [this documentation](https://docs.djangoproject.com/en/1.11/ref/databases/) for more information on SQL engines in Django.

#### Set up nginx

Needs: Nginx

- `sudo vim /etc/nginx/sites-available/default`
- Add site:

```
server {
    listen 80;
    listen [::]:80;

    server_name my.hackupc.com;


    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/user/project_folder/staticfiles/;
    }
    
    location /files/ {
        alias /home/user/project_folder/files/;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/user/project_folder/backend.sock;
    }


}
```

#### Deploy new version

- `git pull`
- `./restart.sh`
- `sudo service backend restart`

### Set up dummy data

TODO: CREATE NEW DUMMY DATA

## Management

### Automated expiration

- Create management.sh from template: `cp management.sh.template management.sh`
- `chmod +x management.sh`
- Edit variables to match your environment and add extra if required (see environment variables available above)
- Add to crontab: `crontab -e`
```
*/5 * * * * cd /home/user/project_folder/ && ./management.sh > /home/user/project_folder/management.log 2> /home/user/project_folder/management_err.log
```

### User roles

- **is_volunteer**: Allows user to check-in hackers with QR and list view
- **is_organizer**: Allows user to vote, see voting ranking and check-in hackers.
- **is_director**: Allows user to send invites to hackers as well as send reimbursement.
- **is_admin**: Allows user to enter Django Admin interface



## Personalization

You can personalize this backend for your hackathon.

### Style

For colors and presentation of views you can edit [app/static/css/main.css](app/static/css/main.css).

To edit the navbar content/disposition you can modify [app/templates/base.html](app/templates/base.html)

The email base template is in [app/templates/base_email.html](app/templates/base_email.html)

### Content

#### Update emails:

You can update emails related to 
- Applications (application invite, event ticket, last reminder) at [applications/templates/mails/](applications/templates/mails/)
- Reimbursements (reimbursement email, reject receipt) at [reimbursement/templates/mails/](reimbursement/templates/mails/)
- User registration (email verification, password reset) at [reimbursement/templates/mails/](reimbursement/templates/mails/)

#### Update hackathon variables
Check all available variables at [app/hackathon_variable.py.template](app/hackathon_variable.py.template). 
You can set the ones that you prefer at [app/hackathon_variable.py](app/hackathon_variable.py)

#### Update registration form
You can change the form, titles, texts in [applications/forms.py](applications/forms.py)

#### Update application model
If you need extra labels for your hackathon, you can change the model and add your own fields.

   - Update model with specific fields:[applications/models.py](applications/models.py)
   - `python manage.py makemigrations`
   - `python manage.py migrate`

# Want to Contribute?
Read these [guidelines](.github/CONTRIBUTING.md) carefully.

By making a contribution, in any form (including, but not limited to, Issues and Pull Requests), you agree to abide by the [Code of Conduct](.github/CODE_OF_CONDUCT.md). Report any incidents to devs@hackcu.org and appropriate action will be taken against the offender after investigation.

# License

MIT © Hackers@UPC

MIT © HackCU
