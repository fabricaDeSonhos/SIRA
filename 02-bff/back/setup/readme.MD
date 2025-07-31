* Setup:

1) Activate the virtual environment:

python3 -m venv sira_back

2) Configure environment variables

Linux:
Execute env.sh

Windows:
TODO

Alternatively, you can run steps 2.1 and 2.2, below.

2.1) You MUST configure PYTHONPATH to make the code works: (update the below path to the path where YOUR source code is)

Linux/macOS
export PYTHONPATH=/home/friend/01-github/SIRA/02-bff/back:$PYTHONPATH

Windows
set PYTHONPATH=C:\path\to\your\project;%PYTHONPATH%

2.2) Export the SIRA_DB environment variable:

Linux:
export SIRA_DB=SQLITE
or
export SIRA_DB=MYSQL

3) Create the database

python3 create_database.py

4) Install requirements (if necessary):

pip3 install -r requirements.txt

* Maintenance: generate new requirements (if necessary):

pip3 freeze > requirements

Otherwise, you can install libraries by hand:

pip3 install flask
pip3 install flask_sqlalchemy
pip3 install flask_cors
pip3 install pytest

5) Run the tests:

in tests folder:
$ python3 basic_tests_/run_basic_tests_.py

in pytest folder:
$ pytest