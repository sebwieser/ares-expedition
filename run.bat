::start backend
start cmd.exe /C "venv\Scripts\activate.bat && cd backend && flask run"

::start frontend
start cmd.exe /C "nodevenv\Scripts\activate.bat && cd frontend && npm start"
