# microblog
Flask tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

## Preparation Win

set path=c:\Users\michael.bach\AppData\Local\Continuum\anaconda3;%path%

## Preparation Mac / Linux

## First run

* git clone https://github.com/ByronBay/app1.git
* python -m venv venv
* source venv/bin/activate
* pip install -r requirements.txt

# Create pip requirements

* pip freeze > requirements.txt

# Jupyter notbeook

* jupyter notebook

# Development Web-Server

* Outputs to console
* python -m smtpd -n -c DebuggingServer localhost:8025

* export MAIL_SERVER=localhost
* export MAIL_PORT=8025

* export MAIL_SERVER=localhost ; export MAIL_PORT=8025

# Flask shell

* flask shell