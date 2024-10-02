# Inventory


cd inventory_mgmt

# Setup Virtual Environment windows

Open Command Prompt

python -m venv venv

Activate the virtual environment

venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv

source venv/bin/activate


pip install -r requirements.txt

# Configure the Database

sudo -u postgres psql


CREATE DATABASE your_database_name;
CREATE USER your_username WITH PASSWORD 'your_password';
ALTER ROLE your_username SET client_encoding TO 'utf8';
ALTER ROLE your_username SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_username SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;


# Update Database Settings: Open settings.py in your project and configure the database settings accordingly:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

python manage.py makemigartions
python manage.py migrate

python manage.py runserver
