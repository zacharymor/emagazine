req python >= 3.8

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
psql -U "postgres" -c "CREATE DATABASE article;"
flask run
