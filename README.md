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
