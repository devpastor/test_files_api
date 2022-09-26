TEST FILE STORAGE API
---------------------

Requirements:
-
- python 3.9
- fastapi >= 0.85.0
- aiofiles >= 22.1.0
- fastapi-restful >= 0.4.3
- uvicorn >= 0.18.3
- python-dotenv >= 0.21.0
- aiocache >= 0.11.1
- ujson >= 5.5.0
- msgpack >= 1.0.4

Setup environment variables:
-

1) Create .env file in the root directory
2) Set the following variables:
   - TEST_FILE_DIR: path to the directory where the test files will be stored
   - DEBUG: set to True to enable debug mode


Install with Poetry:
-
 1) Download & setup Poetry
 2) Create Poetry Venv
 3) `poentry install`
 4) Run main.py
 5) Go to http://localhost:8000/docs

Install with Pip:
-
1) `pip install -r requirements.txt`
2) Run main.py
3) Go to http://localhost:8000/docs