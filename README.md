# Prerequisites
req python >= 3.8


## Steps:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

NOTE: First, uncomment "create_tables_and_sample_data()"... 

Then run:
psql -U "postgres" -c "CREATE DATABASE article;"
flask run
