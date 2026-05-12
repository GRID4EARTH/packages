import json
import subprocess
import textwrap
from typing import Any

import rich_click as click


@click.group()
def main():
    pass


def environment_information(name: str) -> list[dict[str, Any]]:
    proc = subprocess.run(
        ["pixi", "ls", "-x", "-e", name, "--json"], check=True, stdout=subprocess.PIPE
    )
    return json.loads(proc.stdout)


def drop_item(mapping: dict[str, Any], name: str) -> dict[str, Any]:
    copy = dict(mapping)
    copy.pop(name, None)

    return copy


def format_requirements(info: list[dict[str, str]]) -> str:
    return (
        "\n".join([f"{package['name']}=={package['version']}" for package in info])
        + "\n"
    )


def format_conda_environment(
    conda: list[dict[str, str]], pypi: list[dict[str, str]]
) -> str:
    conda_items = [
        f"{p['name']}={p['version']}" if "version" in p else f"{p['name']}"
        for p in conda + [{"name": "pip"}]
    ]
    pypi_items = [f"{p['name']}=={p['version']}" for p in pypi]

    sections = [
        "name: grid4earth",
        "\n".join(["channels:", "- conda-forge"]),
        "\n".join(
            [
                "dependencies:",
                textwrap.indent("\n".join(conda_items), prefix="- "),
                "- pip:",
                textwrap.indent("\n".join(pypi_items), prefix="  - "),
            ]
        ),
    ]
    return "\n".join(sections) + "\n"


@main.command("requirements")
@click.argument("output", default="-", type=click.File("w"))
def requirements(output):
    package_info = environment_information("default")
    exclude = {"python"}

    filtered = [
        {"name": package["name"], "version": package["version"]}
        for package in package_info
        if package["name"] not in exclude
    ]
    formatted = format_requirements(filtered)
    output.write(formatted)


@main.command("conda-environment")
@click.argument("output", default="-", type=click.File("w"))
def conda_environment(output):
    package_info = environment_information("default")
    exclude = {"python"}

    filtered = [
        {"name": p["name"], "version": p["version"], "kind": p["kind"]}
        for p in package_info
        if p["name"] not in exclude
    ]
    conda_packages = [drop_item(p, "kind") for p in filtered if p["kind"] == "conda"]
    pypi_packages = [drop_item(p, "kind") for p in filtered if p["kind"] == "pypi"]
    formatted = format_conda_environment(conda_packages, pypi_packages)
    output.write(formatted)


if __name__ == "__main__":
    main()
