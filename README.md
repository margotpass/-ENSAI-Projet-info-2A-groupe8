# -ENSAI-Projet-info-2A-groupe8

Source code for the ENSAI project "Vous êtes ici..."

Authors : Passard Margot, Courtel Juliette, Guizani Maryem, Kane Mouhamadou Moustapha, Lefrançois Marion

Tutors : Thierry Mathé

Goals:

This application allows you to obtain information about a subdivision or locate a geographic point, only for France.

Service 1: Retrieve a subdivision based on a code
Service 2: Retrieve a subdivision based on a geographic point
Service 3: Retrieve a file containing the subdivision of a list of geographic points

Install
Install the required packages with the following bash commands :
pip install -r requirements.txt     # install all packages listed in the file

pip list                            # to list all installed packages
inquirerPy: Creates interactive command-line interfaces (e.g., prompts and surveys).
pyproj: Performs cartographic projections and geodetic transformations.
typing: Provides type hints and annotations for Python code.
dotenv: Loads environment variables from a .env file.
psycopg2: Connects and interacts with PostgreSQL databases.
psycopg2.extras: Adds advanced features to psycopg2, like support for composite types or query builders.
fiona: Reads and writes spatial data files like shapefiles.
unittest.mock: Mocks objects for testing Python code.
csv: Reads and writes CSV (comma-separated values) files.
pytest : powerful testing framework for Python.
fastapi : FastAPI is a modern web framework for building APIs with high performance.
uvicorn : Uvicorn is a lightning-fast ASGI server implementation.
python-multipart : handles encoding/decoding of multipart/form-data for HTTP requests.

Run :

First option :

python src/app.py

127.0.0.1:8000/docs (in your browser)


Second option :
python src/__main__.py
