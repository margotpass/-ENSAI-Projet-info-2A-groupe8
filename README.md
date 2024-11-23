# **ENSAI - Projet Info 2A - Groupe 8**

### **Source Code**
Source code for the ENSAI project *"Vous êtes ici..."*

### **Authors**
- Passard Margot  
- Courtel Juliette  
- Guizani Maryem  
- Kane Mouhamadou Moustapha  
- Lefrançois Marion  

**Tutors** : Thierry Mathé  

---

### **Goals**
This application allows you to:
1. Obtain information about a subdivision.
2. Locate a geographic point.  
*(Note: The application is limited to France.)*

#### **Services:**
- **Service 1**: Retrieve a subdivision based on a code.  
- **Service 2**: Retrieve a subdivision based on a geographic point.  
- **Service 3**: Retrieve a file containing the subdivision of a list of geographic points.  

---

### **Install**
Install the required packages with the following bash commands:

```bash
pip install -r requirements.txt     # Install all packages listed in the file
pip list                            # List all installed packages
```

# Project Documentation

## Libraries Used:

- **inquirerPy**: Creates interactive command-line interfaces (e.g., prompts and surveys).
- **pyproj**: Performs cartographic projections and geodetic transformations.
- **typing**: Provides type hints and annotations for Python code.
- **dotenv**: Loads environment variables from a `.env` file.
- **psycopg2**: Connects and interacts with PostgreSQL databases.
- **psycopg2.extras**: Adds advanced features to `psycopg2`, like support for composite types or query builders.
- **fiona**: Reads and writes spatial data files like shapefiles.
- **unittest.mock**: Mocks objects for testing Python code.
- **csv**: Reads and writes CSV (comma-separated values) files.
- **pytest**: A powerful testing framework for Python.
- **fastapi**: FastAPI is a modern web framework for building APIs with high performance.
- **uvicorn**: Uvicorn is a lightning-fast ASGI server implementation.
- **python-multipart**: Handles encoding/decoding of multipart/form-data for HTTP requests.

## Run:

### First option:
To run the application, use the following command:

```bash
python src/app.py
```

Then, visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.


### Second option:
Alternatively, you can run the application using this command:
```bash
python src/__main__.py
