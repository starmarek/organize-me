import json
import logging
import os
import platform
import subprocess
import sys
from importlib.metadata import import_module, version
from pathlib import Path

import coloredlogs
import dotenv
import fire
import toml

log = logging.getLogger("admin")
coloredlogs.install(level="DEBUG")

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file, verbose=True, override=True)
with open("Pipfile", "r") as f:
    pipfile = toml.load(f, _dict=dict)


# def assert_python_package(package, to_assert):
#     # assert platform.python_version() == os.environ["PYTHON_VER"], "Please use proper version of python"
#     if version(package) != to_assert:
#         log.warning(
#             f"You should consider using different version of {package}. Actually tested version is {to_assert}"
#         )
# assert (
#     version("python-dotenv") == os.environ["ADMIN_DOTENV_VER"]
# ), "Please use proper version of python-dotenv package"
# assert version("fire") == os.environ["ADMIN_FIRE_VER"], "Please use proper version of fire package"
# assert version("toml") == os.environ["ADMIN_TOML_VER"], "Please use proper version of toml package"
# assert version("pipenv") == os.environ["PIPENV_VER"], "Please use proper version of pipenv package"


# def update_python(ver):
#     dotenv.set_key(dotenv_file, "PYTHON_VER", ver, "")
#     pipfile["requires"]["python_version"] = ver
#     with open("Pipfile", "r+") as f:
#         toml.dump(pipfile, f)
#     os.environ["PIPENV_DONT_USE_PYENV"] = "1"
#     output = subprocess.run(
#         ["pipenv", "update", "--keep-outdated", "--python", ver], capture_output=True, text=True, check=True
#     )
#     print(output.stdout)
#     print(output.stderr)


def build_containers(cache=True):
    log.info("Running build-containers command")
    pass


def run_containers():
    log.info("Running run-containers command")
    pass


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
                json.dump(json_decoded, f)
        except json.JSONDecodeError:
            log.error(f"Couldn't parse your {settings_file} file. Please make sure that it's valid.")
            raise
    print("\033[33m\nIf you use your builtin vscode commandprompt - please restart it\033[0m")


def init(vscode=False):
    log.info("Running init command")
    build_containers()
    run_containers()
    if vscode:
        _update_virtualenv_vscode_pythonpath()


if __name__ == "__main__":
    log.info("Starting admin script")
    fire.Fire()
