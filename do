#!/bin/sh
#set -x

ROOT=$(dirname "$(readlink -f $0)")
SCRIPT=$(basename $0)
VENV="${ROOT}/venv"
PYTHON3="${VENV}/bin/python3"
PIP="${VENV}/bin/pip"
FLASK_VERSION='1.1.1'
IPYTHON_VERSION='7.12.0'
JEDI_VERSION='0.16.0'

_inspect () {
  # Auto generate help string
  local help=$(awk '$1 ~ /^[a-z]+_?[a-z]+$/ && $2 == "()" { printf "%s|", $1 }' $0)
  echo ${help%|}
}

_is_exe () {
  command -v $1 >/dev/null 2>&1 || \
    { echo >&2 "missing $1 command"; return 1; }; return 0
  }
#-----------------------------------------------------------------------------#

_mkvenv () {
  local red=$(tput setaf 1)
  local green=$(tput setaf 2)
  local yellow=$(tput setaf 3)
  local reset=$(tput sgr0)
  printf "Setting up python virtualenv in:\n“${VENV}”\n"
  _is_exe python3 || exit 1
  python3 -m venv "${VENV}"
  printf "→ installing: ${yellow}wheel${reset}…"
  "${PIP}" --quiet install wheel || { echo "${red}Error seting up venv${reset}"; exit 1; }
  printf " ${yellow}flask/${FLASK_VERSION}${reset} & ${yellow}ipython/flask-shell-ipython${reset}…"
  "${PIP}" --quiet install Flask==${FLASK_VERSION} jedi==${JEDI_VERSION} ipython==${IPYTHON_VERSION} flask-shell-ipython || { echo "${red}Error setting up venv${reset}"; exit 1; }
  printf " ${green}done!${reset}\n"
}

_get_jquery () {
  mkdir -p static/js/
  wget -O "${ROOT}/static/js/jquery-3.3.1.min.js" https://code.jquery.com/jquery-3.3.1.min.js
}

_get_bootstrap () {
  mkdir -p "${ROOT}/static/bootstrap"
  wget https://github.com/twbs/bootstrap/releases/download/v4.1.0/bootstrap-4.1.0-dist.zip -O /tmp/bootstrap-4.1.0-dist.zip
  cd "${ROOT}/static/bootstrap" && unzip /tmp/bootstrap-4.1.0-dist.zip && rm /tmp/bootstrap-4.1.0-dist.zip
}
_get_forkawesome () {
  wget https://github.com/ForkAwesome/Fork-Awesome/archive/1.0.11.zip -O  /tmp/1.0.11.zip
  unzip /tmp/1.0.11.zip -d "${ROOT}/static/"
}

get_libs () {
  _get_jquery
  _get_bootstrap
}

serve () {
  #FLASK_APP=app FLASK_ENV=development ${VENV}/bin/flask run
  DEBUG=Y "${PYTHON3}" "${ROOT}/app.py"
}

shell () {
  FLASK_APP=app FLASK_ENV=development "${VENV}/bin/flask" shell -i -c "import app"
}

if [ ! -e "${VENV}/bin/activate" ];then
    _mkvenv
fi
if [ ! -e "${ROOT}/database.db" ];then
  echo "Init sqlite database"
  FLASK_APP=app FLASK_ENV=development "${VENV}/bin/flask" shell -c "import dbmgmt; dbmgmt.init_db();"
fi

if [ $# -eq 0 ]
then
  echo "./${SCRIPT} $(_inspect)"
  exit
fi


$@

# vim: fileencoding=utf8 ft=sh
