#!/bin/zsh

regex="\d{4}.ares_[b|f]e"

server_session_count="$(screen -ls | grep -c -Eo "$regex")"
if [  "$server_session_count" -ne 0 ]; then
  echo "Ares expedition server is already running."
  echo "End existing Screen session(s) before starting new ones:"
  screen -ls | grep -Eo "$regex"
  exit 0
fi

# Remember user's position when running this script
user_wd=$(pwd)
# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

# Position yourself into this script directory
cd "$SCRIPTPATH" || exit 1
screen -S ares_be -dm zsh -c "source venv/bin/activate && cd backend && flask run"
echo "Backend server started..."
screen -S ares_fe -dm zsh -c "source nodevenv/bin/activate && cd frontend && npm start"
echo "Frontend server started..."

echo "You can now attach to either BE or FE process via Screen. i.e. 'screen -R ares_be'."
echo "Available sessions:"
screen -ls | grep -Eo "$regex"

# Return to user's pwd
cd "$user_wd" || exit 1
