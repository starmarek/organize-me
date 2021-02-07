import json
import logging
import os
from pathlib import Path

import dotenv
import ruamel.yaml
import toml

log = logging.getLogger(__name__)


class ProjectFile:
    def __init__(self, path, data_type):
        try:
            self.path = str(Path(path).resolve(strict=True))
        except FileNotFoundError:
            log.warning(f"Path {path} does not exist! This can cause trouble later.")
            self.path = path
        self.name = self.path.split("/")[-1]
        self.desired_data_type = data_type

    def load(self, func, **kwargs):
        try:
            with open(self.path, "r") as f:
                return func(f, **kwargs)
        except FileNotFoundError:
            log.warning(f"Requested file {self.path} is missing. Creating object with empty `data` slot.")
            return None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if not isinstance(value, self.desired_data_type):
            raise TypeError(
                f"Data field of {self} should be of type {self.desired_data_type}. You have tried to set is as {type(value)}"
            )
        self._data = value

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, val):
        try:
            self.data[index] = val
        except TypeError:
            log.error("Can't assing value! Something must be wrong with your file...")
            raise
        except IndexError:
            log.error("Can't set value at that index. Are you sure your file is long enough?")
            raise

    def __repr__(self):
        return f"{type(self).__name__}(path={self.path!r} name={self.name!r})"


class VerifiableFile:
    def __init__(self):
        self.core_versions = {proto: os.environ[proto] for proto in self.core_versions_prototypes.keys()}

    def verify_core_versions(self):
        return all(
            self.core_versions[proto] == self.get_core_version_from_file_data(proto)
            for proto in self.core_versions_prototypes.keys()
        )

    def get_core_version_from_file_data(self, proto):
        data = self
        for item in self.core_versions_prototypes[proto]:
            data = data[item]

        return data


class TomlFile(ProjectFile):
    def __init__(self, path):
        super().__init__(path, dict)
        self._data = super().load(func=toml.load, _dict=dict)

    def dump(self):
        log.info(f"Editing {self}")
        with open(self.path, "w") as f:
            toml.dump(self.data, f)


class JsonFile(ProjectFile):
    def __init__(self, path):
        super().__init__(path, dict)
        try:
            self._data = super().load(func=json.load)
        except json.JSONDecodeError:
            log.error(f"Couldn't parse your {self.path} file. Please make sure that it's valid.")
            raise

    def dump(self):
        log.info(f"Editing {self}")
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)
            f.write("\n")


class YamlFile(ProjectFile):
    def __init__(self, path):
        super().__init__(path, dict)
        self.yaml = ruamel.yaml.YAML()
        self.yaml.width = 4096  # Large number to prevent line wrapping
        self._data, sequence_len, block_len = super().load(
            func=ruamel.yaml.util.load_yaml_guess_indent, preserve_quotes=True
        )
        self.yaml.indent(mapping=block_len, sequence=sequence_len, offset=block_len)

    def dump(self):
        log.info(f"Editing {self}")
        with open(self.path, "w") as f:
            self.yaml.dump(self.data, f)


class DotenvFile(ProjectFile):
    def __init__(self, path):
        super().__init__(path, dict)
        self._data = dotenv.dotenv_values(self.path)
        dotenv.load_dotenv(self.path, verbose=True, override=True)

    def __setitem__(self, index, value):
        log.info(f"Editing {self}")
        self.data[index] = value
        dotenv.set_key(self.path, index, value, "")

    def dump_to_env(self):
        dotenv.load_dotenv(self.path, verbose=True, override=True)


class TxtFile(ProjectFile):
    def __init__(self, path):
        super().__init__(path, list)
        self._data = self.load()

    def load(self):
        try:
            with open(self.path, "r") as f:
                return f.read().splitlines()
        except FileNotFoundError:
            log.warning(f"Requested file {self.path} is missing. Creating object with empty `data` slot.")
            return None

    def dump(self):
        log.info(f"Editing {self}")
        with open(self.path, "w") as f:
            f.write("\n".join(str(item) for item in self.data) + "\n")


class Pipfile(TomlFile, VerifiableFile):
    def __init__(self, path):
        self.core_versions_prototypes = {
            "CORE_PYTHON_VER": ("requires", "python_version"),
        }
        TomlFile.__init__(self, path)
        VerifiableFile.__init__(self)


class GitlabCIFile(YamlFile, VerifiableFile):
    def __init__(self, path):
        self.core_versions_prototypes = {
            "CORE_PYTHON_VER": ("variables", "PYTHON_VERSION"),
            "CORE_NODE_VER": ("variables", "NODE_VERSION"),
        }
        YamlFile.__init__(self, path)
        VerifiableFile.__init__(self)


class DockerComposeFile(YamlFile, VerifiableFile):
    def __init__(self, path):
        self.core_versions_prototypes = {
            "CORE_COMPOSE_VER": ("version",),
        }
        YamlFile.__init__(self, path)
        VerifiableFile.__init__(self)


class YarnRCFile(YamlFile, VerifiableFile):
    def __init__(self, path):
        self.core_versions_prototypes = {
            "CORE_YARN_VER": ("yarnPath",),
        }
        YamlFile.__init__(self, path)
        VerifiableFile.__init__(self)

    def get_core_version_from_file_data(self, proto):
        data = self
        for item in self.core_versions_prototypes[proto]:
            data = data[item]

        return os.path.splitext(data.split("/")[-1])[0].split("-")[1]


class PackageJsonFile(JsonFile, VerifiableFile):
    def __init__(self, path):
        self.core_versions_prototypes = {
            "CORE_NODE_VER": ("engines", "node"),
            "CORE_YARN_VER": ("engines", "yarn"),
        }
        JsonFile.__init__(self, path)
        VerifiableFile.__init__(self)


class RuntimeTxtFile(TxtFile, VerifiableFile):
    def __init__(self, path):
        self.core_versions_prototypes = {
            "CORE_PYTHON_VER": None,
        }
        TxtFile.__init__(self, path)
        VerifiableFile.__init__(self)

    def get_core_version_from_file_data(self, proto):
        return self[0].split("-")[1]
