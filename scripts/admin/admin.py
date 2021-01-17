import json
import logging
import os
import shlex
import subprocess
from pathlib import Path

import coloredlogs
import fire
from adminFiles import DotenvFile, JsonFile, TomlFile, TxtFile, YamlFile

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
    def update_python(self, ver):
        pipfile_file = TomlFile(path="Pipfile")
        dotenv_template_file = DotenvFile(path=".template.env")
        gitlab_ci_file = YamlFile(path=".gitlab-ci.yml")
        runtime_txt_file = TxtFile(path="runtime.txt")

        subprocess.run(["pipenv", "--rm"], check=True)
        pipfile_file["requires"]["python_version"] = ver
        pipfile_file.dump()
        subprocess.run(["pipenv", "update", "--keep-outdated", "--dev"], check=True)

        dotenv_template_file["CORE_PYTHON_VER"] = ver
        dotenv_file["CORE_PYTHON_VER"] = ver
        self.ground_up_containers(cache=False)

        gitlab_ci_file["variables"]["PYTHON_VERSION"] = ver
        gitlab_ci_file.dump()

        runtime_txt_file.data = [f"python-{ver}"]
        runtime_txt_file.dump()

        if running_in_vscode:
            _update_virtualenv_vscode_pythonpath()

    def update_node(self, ver):
        dotenv_template_file = DotenvFile(path=".template.env")
        gitlab_ci_file = YamlFile(path=".gitlab-ci.yml")
        package_json_file = JsonFile(path="package.json")

        dotenv_template_file["CORE_NODE_VER"] = ver
        dotenv_file["CORE_NODE_VER"] = ver

        self.ground_up_containers(cache=False)

        gitlab_ci_file["variables"]["NODE_VERSION"] = ver
        gitlab_ci_file.dump()

        package_json_file["engines"]["node"] = ver
        package_json_file.dump()

    def build_containers(self, cache=True):
        log.info("Running build-containers command")

        subprocess.run(shlex.split(f"docker-compose build --force-rm {'' if cache else '--no-cache'}"), check=True)

    def run_containers(self):
        log.info("Running run-containers command")

        subprocess.run(shlex.split("docker-compose up --detach --remove-orphans --force-recreate"), check=True)

    def ground_up_containers(self, cache=True):
        log.info("Running ground-up-containers command")

        self.build_containers(cache=cache)
        self.run_containers()

    def init(self):
        log.info("Running init command")

        self.ground_up_containers(cache=False)
        if running_in_vscode:
            _update_virtualenv_vscode_pythonpath()


if __name__ == "__main__":
    log.info("Starting admin script")
    fire.Fire(CLI)
