# grid4earth packages

This repository provides requirement files that can be used to install a curated set of the packages developed as part of the Grid4Earth project.

## Usage

To install a particular version with `pip`, use (replacing `2026.05.4` with the desired release):

```sh
wget -q https://github.com/GRID4EARTH/packages/releases/download/v2026.05.4/requirements.txt
pip install -r requirements.txt
```

Or, with conda:

```sh
wget -q https://github.com/GRID4EARTH/packages/releases/download/v2026.05.4/env.yml
conda env update -f env.yml -n <env>
```

## How to update

To update the registry, run `pixi update` in a new branch:

```sh
git pull
git switch -c bump
pixi update
git add pixi.lock
git commit -m "bump grid4earth packages"
git push origin bump
```

Then create a pull request and merge it after CI passes.

After that, all that is necessary is create a release using github's web interface or the CLI:

```sh
gh release create v<version> -n "Release v<version>"
```

The CI will then add the necessary release artifacts.
