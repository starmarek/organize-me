#! /usr/bin/env bash


if [[ -f .env ]]; then
    export $(cat .env | sed 's/#.*//g'| xargs)
else
    echo -e "\e[91mERROR: You need to create your .env file first!\e[0m"
    exit
fi


pipenv_version=($(pipenv --version 2> /dev/null))
if [[ -z "${pipenv_version[2]}" ]]; then
    echo -e "\e[91mERROR: You need to install pipenv first!\e[0m"
    exit
elif [[ "${pipenv_version[2]}" != "${CORE_PIPENV_VER}" ]]; then
    echo -e "\e[33mWARNING: We highly recommend to use tested pipenv version --> ${CORE_PIPENV_VER}\e[0m"
fi


if ! pipenv --venv &> /dev/null; then
    pipenv sync --dev
fi


python_path=$(pipenv run which python 2> /dev/null)
${python_path} scripts/admin.py $@
