
# Setup

## macOS

```
$ ssh-keygen -t rsa -b 4096 -C "josh@schultheiss.io"
# press enter 3 times
$ pbcopy < ~/.ssh/id_rsa.pub
# Copies the contents of the id_rsa.pub file to your clipboard
$ mkdir Developer
# Make a directory to hold your development work
$ cd Developer
# go into it
$ git
# install required devtools
$ git clone git@github.com:0x213F/jukebox-radio.git
# yes
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
$ brew install python3
$ pip3 install --upgrade pip
$ pip3 install virtualenv --user
$ virtualenv -p python3 venv
$ brew install redis
$ brew services start redis
$ brew install rabbitmq
$ brew services start rabbitmq
```

```
git
sudo easy_install pip
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
sudo -H pip install virtualenv
git clone https://github.com/0x213F/django-boilerplate
cd django-boilerplate
virtualenv venv
source venv/bin/activate
https://www.python.org/downloads/release/python-372/
pip3 install -r requirements.txt
brew install postgres
brew tap homebrew/services
brew services start postgresql
createdb chess
psql postgres
CREATE USER dev WITH PASSWORD 'password';
ALTER USER dev CREATEDB;
ALTER ROLE dev SET client_encoding TO 'utf8';
ALTER ROLE dev SET default_transaction_isolation TO 'read committed';
ALTER ROLE dev SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE chess TO dev;
\q
python3 manage.py makemigrations user
python3 manage.py migrate
# python3 manage.py createsuperuser
export DJANGO_SETTINGS_MODULE=proj.settings
python3 manage.py runserver
```
