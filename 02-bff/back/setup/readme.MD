* Setup:

Go to the folder SIRA/02-bff/back, in terminal

1) OPTIONAL: activate the virtual environment:

Linux:
source setup/venv/bin/activate

Windows: 
TODO

2) IF you want to run the tests, configure environment variables:

a) You MUST configure PYTHONPATH to make the tests work: (update the below path to the path where YOUR source code is)

Linux/macOS
export PYTHONPATH=/home/friend/01-github/SIRA/02-bff/back:$PYTHONPATH

Windows
set PYTHONPATH=C:\path\to\your\project;%PYTHONPATH%

b) If you want to use MYSQL, export the SIRA_DB environment variable:

Linux:
export SIRA_DB=MYSQL

Windows: 
TODO

3) You can remove the sira.bd file and re-create the database:

rm src/sira.db

python3 setup/create_database.py

4) Install requirements (if necessary):

pip3 install -r requirements.txt

* Alternatively, you can install libraries by hand:

pip3 install flask
pip3 install flask_sqlalchemy
pip3 install flask_cors
pip3 install pytest
pip3 install flask_jwt_extended

* Maintenance: when necessary, generate new requirements:

pip3 freeze > requirements

5) OPTIONAL: run the backend tests:

$ python3 tests/basic_tests_/run_basic_tests_.py

$ pytest -s

6) Now you can run the backend :-)

In folder "SIRA/02-bff/back/src", run:

flask run --debug

7) After start the backend, you can also, in another terminal, run basic web tests:

In the "back" folder:

$ python3 tests/basic_tests_/web/basic_web_tests_.py 
