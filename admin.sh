#! /usr/bin/env bash


if [[ -f .env ]]; then
    # shellcheck disable=SC2046
    export $(sed 's/#.*//g' .env | xargs)
else
    echo -e "\e[91mERROR: You need to create your .env file first!\e[0m"
    exit 1
fi


IFS=" " read -r -a pipenv_version_array <<< "$(pipenv --version 2> /dev/null)"
if [[ -z "${pipenv_version_array[2]}" ]]; then
    echo -e "\e[91mERROR: You need to install pipenv first!\e[0m"
    exit 1
elif [[ "${pipenv_version_array[2]}" != "${CORE_PIPENV_VER}" ]]; then
    echo -e "\e[33mWARNING: We highly recommend to use tested pipenv version --> ${CORE_PIPENV_VER}\e[0m"
fi


if ! pipenv --venv &> /dev/null; then
    pipenv sync --dev || exit 1
fi

# force to run outside virtualenv
if [[ -n ${VIRTUAL_ENV} ]]; then
    # shellcheck disable=SC1091
    source deactivate
fi

python_path=$(pipenv run which python 2> /dev/null)
${python_path} scripts/admin.py "$@"
