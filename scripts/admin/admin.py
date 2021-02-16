import json
import logging
import os
import shlex
import subprocess
from pathlib import Path
from types import SimpleNamespace

import coloredlogs
import fire

from .adminFiles import (
    DockerComposeFile,
    DotenvFile,
    GitlabCIFile,
    JsonFile,
    PackageJsonFile,
    Pipfile,
    RuntimeTxtFile,
    YarnRCFile,
)

log = logging.getLogger("admin")
coloredlogs.install(level="DEBUG")

yarn_dir = ".yarn/releases/"
for file in os.listdir(".yarn/releases"):
    if os.getenv("CORE_YARN_VER") in file:
        yarn_executable = file

dotenv_file = DotenvFile(path=".env")
compose_file = DockerComposeFile(path="docker-compose.yml")
dotenv_template_file = DotenvFile(path=".template.env")
gitlab_ci_file = GitlabCIFile(path=".gitlab-ci.yml")
yarnrc_file = YarnRCFile(path=".yarnrc.yml")
runtime_txt_file = RuntimeTxtFile(path="runtime.txt")
pipfile_file = Pipfile(path="Pipfile")
package_json_file = PackageJsonFile(path="package.json")
verifiable_files = [compose_file, gitlab_ci_file, pipfile_file, runtime_txt_file, package_json_file, yarnrc_file]


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
    log.info(f"Setting vscode pythonpath to '{virtualenv_path}/bin/python'")


def _verify_dotenvs():
    log.info("Verifying dotenvs compatibility")
    assert all(val == dotenv_template_file[key] for key, val in dotenv_file.data.items() if key.startswith("CORE"))


def _verify_yarn_executable():
    log.info("Verifying yarn compatibility")
    assert any(os.getenv("CORE_YARN_VER") in yarn_executable for yarn_executable in os.listdir(".yarn/releases"))


def _verify_versions():
    curr = dotenv_file
    reference = dotenv_template_file
    try:
        _verify_dotenvs()

        reference = dotenv_file
        curr = SimpleNamespace(name="files in .yarn/releases dir")
        _verify_yarn_executable()

        log.info("Verifying compatibility of core versions")
        for ver_file in verifiable_files:
            curr = ver_file
            assert ver_file.verify_core_versions()
    except AssertionError:
        log.error(
            f"There is a mismatch between {curr.name} and {reference.name}! Make sure that you are using admin script to bump versions of packages!"
        )
        raise


class CLI:
    def __init__(self, vscode=False):
        try:
            self.running_in_vscode = os.environ["TERM_PROGRAM"] == "vscode"
        except KeyError:
            self.running_in_vscode = False

        if vscode:
            self.running_in_vscode = True

    def update_yarn(self, ver):
        log.info("Upgrading yarn")

        subprocess.run([yarn_dir + yarn_executable, "set", "version", ver], check=True)

        dotenv_template_file["CORE_YARN_VER"] = ver
        dotenv_file["CORE_YARN_VER"] = ver
        dotenv_file.dump_to_env()

        package_json_file["engines"]["yarn"] = ver
        package_json_file.dump()

        self.containers_ground_up(cache=False)

    def update_postgres(self, ver):
        dotenv_template_file["CORE_POSTGRES_VER"] = ver
        dotenv_file["CORE_POSTGRES_VER"] = ver
        dotenv_file.dump_to_env()

        self.containers_ground_up(cache=False)

    def update_compose(self, ver):
        ver = str(ver)

        dotenv_template_file["CORE_COMPOSE_VER"] = ver
        dotenv_file["CORE_COMPOSE_VER"] = ver
        dotenv_file.dump_to_env()

        compose_file["version"] = ver
        compose_file.dump()

        self.containers_ground_up(cache=False)

    def update_python(self, ver):
        log.info("Reinstalling your pipenv")
        subprocess.run(["pipenv", "--rm"], check=True)
        pipfile_file["requires"]["python_version"] = ver
        pipfile_file.dump()
        subprocess.run(["pipenv", "update", "--keep-outdated", "--dev"], check=True)

        dotenv_template_file["CORE_PYTHON_VER"] = ver
        dotenv_file["CORE_PYTHON_VER"] = ver
        dotenv_file.dump_to_env()
        self.containers_ground_up(cache=False)

        gitlab_ci_file["variables"]["PYTHON_VERSION"] = ver
        gitlab_ci_file.dump()

        runtime_txt_file.data = [f"python-{ver}"]
        runtime_txt_file.dump()

        if self.running_in_vscode:
            _update_virtualenv_vscode_pythonpath()

    def update_node(self, ver):
        dotenv_template_file["CORE_NODE_VER"] = ver
        dotenv_file["CORE_NODE_VER"] = ver
        dotenv_file.dump_to_env()

        self.containers_ground_up(cache=False)

        gitlab_ci_file["variables"]["NODE_VERSION"] = ver
        gitlab_ci_file.dump()

        package_json_file["engines"]["node"] = ver
        package_json_file.dump()

    def containers_build(self, cache=True):
        log.info(f"Building containers with 'cache={cache}'")
        subprocess.run(shlex.split(f"docker-compose build --force-rm {'' if cache else '--no-cache'}"), check=True)

    def containers_logs(self, container_name=""):
        try:
            subprocess.run(shlex.split(f"docker-compose logs -f {container_name}"))
        except KeyboardInterrupt:
            pass

    def containers_up(self):
        log.info("Running containers")
        subprocess.run(shlex.split("docker-compose up --detach --remove-orphans --force-recreate"), check=True)

    def containers_ground_up(self, cache=True):
        self.containers_build(cache=cache)
        self.containers_up()

    def init(self):
        self.containers_ground_up(cache=False)
        if self.running_in_vscode:
            _update_virtualenv_vscode_pythonpath()

    def install_pip(self, package, dev):
        subprocess.run(["pipenv", "install", package, "--dev" if dev else ""], check=True)

        self.containers_ground_up(cache=False)

    def install_yarn(self, package, dev):
        subprocess.run(["sudo", yarn_dir + yarn_executable, "add", package, "--dev" if dev else ""], check=True)

        self.containers_ground_up(cache=False)

    def remove_pip(self, package):
        subprocess.run(["pipenv", "uninstall", package], check=True)

        self.containers_ground_up(cache=False)

    def remove_yarn(self, package):
        subprocess.run(["sudo", yarn_dir + yarn_executable, "remove", package], check=True)

        self.containers_ground_up(cache=False)


if __name__ == "__main__":
    log.info("Starting admin script")
    _verify_versions()
    fire.Fire(CLI)
