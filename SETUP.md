# Lineup [name pending]

## macOS

```
git
sudo easy_install pip
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
sudo -H pip install virtualenv
git clone https://github.com/0x213F/rock-paper-scissors
cd rock-paper-scissors/
virtualenv venv
source venv/bin/activate
https://www.python.org/downloads/release/python-372/
pip3 install -r requirements.txt
brew install postgres
brew tap homebrew/services
brew services start postgresql
createdb lineup
psql postgres
CREATE USER dev WITH PASSWORD 'password';
ALTER USER dev CREATEDB;
ALTER ROLE dev SET client_encoding TO 'utf8';
ALTER ROLE dev SET default_transaction_isolation TO 'read committed';
ALTER ROLE dev SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE lineup TO dev;
\q
python3 manage.py makemigrations user
python3 manage.py migrate
# python3 manage.py createsuperuser
export DJANGO_SETTINGS_MODULE=lineup.settings
python3 manage.py runserver
```
