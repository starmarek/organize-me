import json
import logging
from pathlib import Path

import dotenv
import ruamel.yaml
import toml

log = logging.getLogger(__name__)


class ProjectFile:
    def __init__(self, path, data_type):
        try:
            self._path = str(Path(path).resolve(strict=True))
        except FileNotFoundError:
            log.warning(f"Path {path} does not exist! This can cause trouble later.")
            self._path = path
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
    def path(self):
        return self._path

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


class TomlFile(ProjectFile):
    def __init__(self, path):
        super().__init__(path, dict)
        self._data = super().load(func=toml.load, _dict=dict)

    def dump(self):
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
        with open(self.path, "w") as f:
            self.yaml.dump(self.data, f)


class DotenvFile(ProjectFile):
    def __init__(self, path):
        super().__init__(path, dict)
        self._data = dotenv.dotenv_values(self.path)
        dotenv.load_dotenv(self.path, verbose=True, override=True)

    def __setitem__(self, index, value):
        self.data[index] = value
        dotenv.set_key(self.path, index, value, "")
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
        with open(self.path, "w") as f:
            f.write("\n".join(str(item) for item in self.data) + "\n")
