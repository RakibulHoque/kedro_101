#!/bin/bash
DEPLOYMENT=${1:-"local"}
TOOL_FOLDER=${3:-"_101"}

# EXECUTION_DIRECTORY=$(dirname $(realpath $0))
EXECUTION_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"     # written this way for windows
cd $EXECUTION_DIRECTORY

case $DEPLOYMENT in
    prod)
    ROOT_PROJECT_DIR=/src
    DOT_ENV_FILE=$EXECUTION_DIRECTORY/.env.$DEPLOYMENT
    ;;
    stage)
    ROOT_PROJECT_DIR=/src
    DOT_ENV_FILE=$EXECUTION_DIRECTORY/.env.$DEPLOYMENT
    ;;
    *)
    ROOT_PROJECT_DIR=$EXECUTION_DIRECTORY
    DOT_ENV_FILE=$ROOT_PROJECT_DIR/.env.$DEPLOYMENT
esac

TOOL_PROJECT_DIR=$ROOT_PROJECT_DIR/$TOOL_FOLDER




function log() {
    echo -e "$(date +"%Y-%m-%dT%H:%M:%S%z") INFO $@"
}

function warn() {
    echo -e "$(date +"%Y-%m-%dT%H:%M:%S%z") WARNING $@"
}

function error() {
    echo -e "$(date +"%Y-%m-%dT%H:%M:%S%z") ERROR $@"
    exit 1
}

function create_dot_env() {
  if [ -f "$DOT_ENV_FILE" ]
    then
      warn "$DOT_ENV_FILE file already exists."
      warn "Overwriting the existing $DOT_ENV_FILE file."
  fi
  (
      echo "DEPLOYMENT=$DEPLOYMENT"
      echo "ROOT_PROJECT_DIR=$ROOT_PROJECT_DIR"
      echo "TOOL_PROJECT_DIR=$TOOL_PROJECT_DIR"
      echo "KEDRO_ENV"="dev"
  ) > "$DOT_ENV_FILE"
  log "$DOT_ENV_FILE file created"
}

function create_python_venv() {
      if [ -d "$ROOT_PROJECT_DIR/venv" ]
      then
          log "Directory $ROOT_PROJECT_DIR/venv exists."
      else
          log "Creating virtual environment for os:$OSTYPE"
          if [[ "$OSTYPE" == "linux-gnu"* ]]; then
              python -m venv venv
          elif [[ "$OSTYPE" == "darwin"* ]]; then
              python3 -m venv venv      # Mac OSX
          elif [[ "$OSTYPE" == "cygwin" ]]; then
              python -m venv venv      # POSIX compatibility layer and Linux environment emulation for Windows
          elif [[ "$OSTYPE" == "msys" ]]; then
              python -m venv venv      # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
          elif [[ "$OSTYPE" == "freebsd"* ]]; then
              python -m venv venv
          else
              log "Unknown os version, trying to install venv..."
              python -m venv venv      # Unknown
          fi
          log "Virtual environment created"
      fi
      log "Activating virtual environment"
      source venv/bin/activate
      log "Virtual environment activated successfully, Now installing requirements..."
      pip install -r requirements.txt
      log "Requirements installed successfully"
}

case $DEPLOYMENT in
  local|dev|qa)
    create_python_venv
    ;;
  stage|prod)
      log "stage|dev|prod do not require virtual environment creation."
    ;;
    *)
      error "Invalid deployment $DEPLOYMENT. It must be within [local, stage, dev, qa, prod]"
esac &&
create_dot_env &&
case $DEPLOYMENT in
  prod)
    export_env_file="$EXECUTION_DIRECTORY/.env.prod"
    ;;
  *)
    export_env_file="$DOT_ENV_FILE"
esac &&
if [ -f "$export_env_file" ]
  then
  # shellcheck disable=SC2046
  export $(xargs < "$export_env_file")
  log "Exported below mentioned environment variables.\n\n$(cat "$export_env_file")\n
  Congratulations, setup process completed."
else
  error "Failed to export environment variables. $export_env_file file does not exist. for prod, stage must be invoked before prod."
fi