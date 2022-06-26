::install backend
venv\Scripts\activate.bat
pip install -r requirements.txt

::install frontend
nodeenv -n 16.15.1 nodevenv
nodevenv\Scripts\activate.bat
cd frontend && npm install