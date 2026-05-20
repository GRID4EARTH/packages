import json
import pathlib
import re
import subprocess

import rich_click as click

dependencies_re = re.compile(r"(?P<name>[-a-z]+)==(?P<version>[0-9]+(?:\.[0-9]+)*)")


def replace_version(match, packages):
    name = match.group("name")

    return f"{name}=={packages[name]}"


@click.command
def main():
    proc = subprocess.run(
        ["pixi", "ls", "-x", "-e", "default", "--json"],
        check=True,
        stdout=subprocess.PIPE,
    )
    package_info = json.loads(proc.stdout)
    exclude = {"python"}

    filtered = {
        p["name"].replace("_", "-"): p["version"]
        for p in package_info
        if p["name"] not in exclude
    }

    pyproject_path = pathlib.Path("pyproject.toml")

    package_metadata = pyproject_path.read_text()
    replaced = dependencies_re.sub(
        lambda m: replace_version(m, filtered), package_metadata
    )

    pyproject_path.write_text(replaced)


if __name__ == "__main__":
    main()
