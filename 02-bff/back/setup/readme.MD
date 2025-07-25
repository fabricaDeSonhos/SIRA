* Setup:

1) Install requirements:

pip install -r requirements.txt

* Maintenance: generate new requirements (if necessary):

pip freeze > requirements

2) You MUST configure PYTHONPATH to make the code works: (update the below path to the path where YOUR source code is)

Linux/macOS
export PYTHONPATH=/home/friend/01-github/SIRA/02-bff/back:$PYTHONPATH

Windows
set PYTHONPATH=C:\path\to\your\project;%PYTHONPATH%

3) Create the database

python create_database.py