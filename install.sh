# install backend
source venv/bin/activate
pip install -r requirements.txt

# install frontend
#   OSX: if this throws CERTIFICATE_VERIFY_FAILED error, you may need to follow instructions to install
#   the SSL certificates: https://stackoverflow.com/a/42334357
nodeenv -n 16.15.1 nodevenv
source nodevenv/bin/activate
cd frontend && npm install

deactivate # to deactivate both virtual environments
