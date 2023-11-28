import click
import os
import sys
from importlib import import_module


class Root:
    def __init__(self, base_dir="cli"):
        print(sys.path)
        print(os.getcwd())
        self.base_dir = base_dir
        self.base_path = os.path.join(os.getcwd(), base_dir)

        root = self.root
        self._load_commands(root)
        root()

    @click.group()
    def root():
        """Base cli"""

    def _load_commands(self, root: click.Group):
        for item in os.listdir(self.base_dir):
            if Group.is_valid(item, self.base_dir):
                group = Group(item, self.base_dir)
                root.add_command(group.get())

            if Command.is_valid(item, self.base_dir):
                command = Command(item, self.base_dir)
                root.add_command(command.get())


class Group:
    def __init__(self, name: str, directory: str) -> None:
        # Construct the module path and extract the name of the command
        self.module_name = f"{directory.replace('/', '.')}.{name}"
        self.module_path = os.path.join(directory, name)
        self.name = name

    def get(self):
        # Dynamically import the module and return a Click command
        imported_module = import_module(self.module_name)
        base_group = click.group()(getattr(imported_module, self.name, None))

        for item in os.listdir(self.module_path):
            if Group.is_valid(item, self.module_path):
                group = Group(item, self.module_path)
                base_group.add_command(group.get())

            if Command.is_valid(item, self.module_path):
                command = Command(item, self.module_name)
                base_group.add_command(command.get())

        return base_group

    @staticmethod
    def is_valid(item: str, path: str):
        return not item.startswith("__") and os.path.isdir(os.path.join(path, item))


class Command:
    def __init__(self, name: str, directory: str) -> None:
        # Remove .py from name
        self.name = name[:-3] if name.endswith(".py") else name
        self.directory = directory

    def get(self):
        # Dynamically import the module and return a Click command
        imported_module = import_module(f"{self.directory}.{self.name}")
        return click.command()(getattr(imported_module, self.name, None))

    @staticmethod
    def is_valid(item: str, path: str):
        return (
            not item.startswith("__")
            and item.endswith(".py")
            and os.path.isfile(os.path.join(path, item))
        )


if __name__ == "__main__":
    Root()
