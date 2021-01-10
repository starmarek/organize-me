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
from adminFiles import DotenvFile, JsonFile, TomlFile, YamlFile

log = logging.getLogger("admin")
coloredlogs.install(level="DEBUG")

dotenv_file = DotenvFile(path=".env")
running_in_vscode = os.environ["TERM_PROGRAM"] == "vscode"


def _update_virtualenv_vscode_pythonpath():
    settings_file = JsonFile(path=".vscode/settings.json")
    virtualenv_path = subprocess.run(["pipenv", "--venv"], capture_output=True, text=True, check=True).stdout.strip()

    Path(settings_file.path.split("/")[-2]).mkdir(exist_ok=True)
    if Path(settings_file.path).exists():
        settings_file["python.pythonPath"] = f"{virtualenv_path}/bin/python"
        settings_file.dump()
    else:
        settings_file.data = json.loads(json.dumps({"python.pythonPath": f"{virtualenv_path}/bin/python"}))
        settings_file.dump()


class CLI:
    def update(self, item):
        log.info("Running update command")

        update_func_map = {
            "python": _update_python,
            "node": _update_node,
            "compose": _update_compose,
            **dict.fromkeys(
                ["postgres", "pipenv"],
                _regular_update,
            ),
        }

    def _regular_update(self, item, ver):
        pass

    def update_compose(self, item, ver):
        pass

    def _update_python(self, ver):
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

        if running_in_vscode:
            _update_virtualenv_vscode_pythonpath()

    def _update_node(self, ver):
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

    def build_containers(self, cache=True):
        log.info("Running build-containers command")

        subprocess.run(
            shlex.split(f"docker-compose build --force-rm --parallel {'' if cache else '--no-cache'}"), check=True
        )

    def run_containers(self):
        log.info("Running run-containers command")

        subprocess.run(shlex.split("docker-compose up --detach --remove-orphans --force-recreate"), check=True)

    def ground_up_containers(self, cache=True):
        log.info("Running ground-up-containers command")

        build_containers(cache=cache)
        run_containers()

    def init(self):
        log.info("Running init command")

        # ground_up_containers(cache=False)
        if running_in_vscode:
            _update_virtualenv_vscode_pythonpath()

    def dummy(self):
        dd = JsonFile(str(Path(".vscode/settings.json").resolve()))
        exit()
        dd["POSTGRES_DB"] = "joachim"
        print(dd["POSTGRES_DB"])
        print(dd)


if __name__ == "__main__":
    log.info("Starting admin script")
    fire.Fire()
