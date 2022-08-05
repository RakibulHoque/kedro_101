#!/bin/bash
# Written in windows 10 linux. So, change the venv section according to os.
readonly DEPLOYMENT=${1:-"local"}

function log() {
    echo -e "$(date +"%Y-%m-%dT%H:%M:%S%z") INFO $@"
}

function error() {
    echo -e "$(date +"%Y-%m-%dT%H:%M:%S%z") ERROR $@"
    exit 1
}

function import_dotenv() {
    set -o allexport
    source .env set
    +o allexport
    log "Environment variables imported in local script"
}

function show_arguments() {
    log "Running with the following arguments:
    deployment : $DEPLOYMENT
    project dir : $ROOT_PROJECT_DIR
    gcloud service key: $GCLOUD_SERVICE_JSON
    "
}

function create_python_venv() {
    local venv_path="$ROOT_PROJECT_DIR/venv"
    echo $venv_path
    if [ -d $venv_path ]
    then 
        log "venv folder exists. Path: $venv_path"
    else
        log "creating venv in $(python --version)..."
        python -m venv venv # Windows specific command
        log "venv created!"
    fi
}

function activate_venv() {
    log "activating virtual environment"
    source venv/Scripts/activate # Windows specific command
    log "venv activated."
}

function setup_venv() {
    log "installing requirements.txt"
    pip install --no-deps -r requirements.txt
    log "python requirements installed."
}

function main() {
    import_dotenv
    show_arguments
    case $DEPLOYMENT in
    local)
        create_python_venv
        activate_venv
        setup_venv
        ;;
    stage|dev|prod)
        log "stage|dev|prod is under development"
        ;;
    *)
    error "Invalid deployment $DEPLOYMENT. It must be within [local, stage, dev, prod]"
    esac
}

main