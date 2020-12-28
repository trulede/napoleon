# Napoleon

Napoleon Sphinx Documentation Build Container Image.

[![Release](https://github.com/trulede/napoleon/workflows/Release/badge.svg)](https://github.com/trulede/napoleon/releases/latest)
![Super Linter](https://github.com/trulede/napoleon/workflows/Super%20Linter/badge.svg)
![Main CI](https://github.com/trulede/napoleon/workflows/Main%20CI/badge.svg)


## Overview

### Python Module

```bash
git clone https://github.com/trulede/napoleon.git
cd napoleon
make
make install
napoleon --git_repo https://github.com/trulede/sphinx-example.git
```

### Docker Container

```bash
git clone https://github.com/trulede/napoleon.git
cd napoleon
make
make docker
docker run --env NAPOLEON_GIT_REPO=https://github.com/trulede/sphinx-example.git napoleon:latest
```

## Details

### Layout of Documentation Project

Directory/File | Environment Variable | Description
-------------- | -------------------- | -----------
proj | NAPOLEON_REPO_DIR | All paths relative to this.
proj/module | NAPOLEON_MODULE_DIRS | Modules and Package directories to build API Doc for.
proj/doc/source | NAPOLEON_SOURCE_DIR | Directory where the conf.py file is located.
proj/doc/source/conf.py | - | This file is generated if not present.
proj/doc/source/index.rst | - | This file is generated if conf.py is not present.
proj/doc/build | NAPOLEON_BUILD_DIR | Build output is placed in this directory (typically under the html subdirectory).


### Sphinx Tools

#### Sphinx API-Doc

sphinx-apidoc -f -o source/ ../binary_trees/


#### Sphinx Build

sphinx-build -M html source build


### Testing Build Output (html)

Test with this command, from build/html:
    python -m http.server
