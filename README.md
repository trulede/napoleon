# Napoleon

Napoleon Sphinx Documentation Build Container Image.

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

    proj                              REPODIR .. paths relative to this.
    proj/module                       MODULEDIRS
    proj/doc/source                   SOURCEDIR
    proj/doc/source/conf.py           ** generated
    proj/doc/source/index.rst         ** generated, with modules.
    proj/doc/build                    BUILDDIR .. the output is under html


### Sphinx Tools

#### Sphinx API-Doc

sphinx-apidoc -f -o source/ ../binary_trees/


#### Sphinx Build

sphinx-build -M html source build


### Testing Build Output (html)

Test with this command, from build/html:
    python -m http.server
