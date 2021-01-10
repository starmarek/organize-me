import json
import logging
import os
import shlex
import subprocess
from pathlib import Path

import coloredlogs
import dotenv
import fire
import ruamel.yaml
import toml

log = logging.getLogger("admin")
coloredlogs.install(level="DEBUG")

dotenv_file = dotenv.find_dotenv()
dotenv_template = dotenv.find_dotenv(".template.env")
dotenv.load_dotenv(dotenv_file, verbose=True, override=True)

with open("Pipfile", "r") as f:
    pipfile = toml.load(f, _dict=dict)

with open(".gitlab-ci.yml", "r") as f:
    gitlab_ci, sequence, block = ruamel.yaml.util.load_yaml_guess_indent(f, preserve_quotes=True)
yaml = ruamel.yaml.YAML()
yaml.width = 4096
yaml.indent(mapping=block, sequence=sequence, offset=block)


def update_python(ver):
    log.info("Running update_python command")

    subprocess.run(["pipenv", "--rm"], check=True)
    pipfile["requires"]["python_version"] = ver
    with open("Pipfile", "r+") as f:
        toml.dump(pipfile, f)
    subprocess.run(["pipenv", "update", "--keep-outdated", "--dev"], check=True)

    dotenv.set_key(dotenv_file, "CORE_PYTHON_VER", ver, "")
    dotenv.set_key(dotenv_template, "CORE_PYTHON_VER", ver, "")
    dotenv.load_dotenv(dotenv_file, verbose=True, override=True)
    ground_up_containers(False)

    gitlab_ci["variables"]["PYTHON_VERSION"] = ver
    with open(".gitlab-ci.yml", "r+") as f:
        yaml.dump(gitlab_ci, f)

    with open("runtime.txt", "w") as f:
        f.write(f"python-{ver}\n")

    if os.environ["TERM_PROGRAM"] == "vscode":
        _update_virtualenv_vscode_pythonpath()


def update_node(ver):
    log.info("Running update_node command")

    dotenv.set_key(dotenv_file, "CORE_NODE_VER", ver, "")
    dotenv.set_key(dotenv_template, "CORE_NODE_VER", ver, "")
    dotenv.load_dotenv(dotenv_file, verbose=True, override=True)
    ground_up_containers(cache=False)

    gitlab_ci["variables"]["NODE_VERSION"] = ver
    with open(".gitlab-ci.yml", "r+") as f:
        yaml.dump(gitlab_ci, f)

    with open("package.json", "r") as f:
        data = json.load(f)
    data["engines"]["node"] = ver
    with open("package.json", "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def build_containers(cache=True):
    log.info("Running build-containers command")

    subprocess.run(
        shlex.split(f"docker-compose build --force-rm --parallel {'' if cache else '--no-cache'}"), check=True
    )


def run_containers():
    log.info("Running run-containers command")

    subprocess.run(shlex.split("docker-compose up --detach --remove-orphans --force-recreate"), check=True)


def ground_up_containers(cache=True):
    log.info("Running ground-up-containers command")

    build_containers(cache=cache)
    run_containers()


def _update_virtualenv_vscode_pythonpath():
    settings_file = ".vscode/settings.json"
    virtualenv_path = subprocess.run(["pipenv", "--venv"], capture_output=True, text=True, check=True).stdout.strip()

    Path(settings_file.split("/")[0]).mkdir(exist_ok=True)
    if not os.path.exists(settings_file):
        with open(settings_file, "w") as f:
            to_dump = {"python.pythonPath": f"{virtualenv_path}/bin/python"}
            json.dump(json.loads(json.dumps(to_dump)), f)
    else:
        try:
            with open(settings_file) as f:
                json_decoded = json.load(f)
            json_decoded["python.pythonPath"] = f"{virtualenv_path}/bin/python"
            with open(settings_file, "w") as f:
                json.dump(json_decoded, f, indent=2)
        except json.JSONDecodeError:
            log.error(f"Couldn't parse your {settings_file} file. Please make sure that it's valid.")
            raise


def init():
    log.info("Running init command")

    ground_up_containers(cache=False)
    if os.environ["TERM_PROGRAM"] == "vscode":
        _update_virtualenv_vscode_pythonpath()


if __name__ == "__main__":
    log.info("Starting admin script")
    fire.Fire()
