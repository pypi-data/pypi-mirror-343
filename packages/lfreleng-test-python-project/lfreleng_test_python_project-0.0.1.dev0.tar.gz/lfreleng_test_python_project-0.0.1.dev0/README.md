# Test Python Project

<!--
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation
-->

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD013 -->
[![Linux Foundation](https://img.shields.io/badge/Linux-Foundation-blue)](https://linuxfoundation.org//) [![Source Code](https://img.shields.io/badge/GitHub-100000?logo=github&logoColor=white&color=blue)](https://github.com/lfreleng-actions/test-python-project) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![pre-commit.ci status badge]][pre-commit.ci results page] [![PyPI](https://img.shields.io/pypi/v/lfreleng-test-python-project?logo=python&logoColor=white&color=blue)](https://pypi.org/project/lfreleng-test-python-project) [![testpypi](https://img.shields.io/pypi/v/lfreleng-test-python-project?logo=python&label=testpypi&logoColor=white&color=32C955&pypiBaseUrl=https://test.pypi.org)](https://test.pypi.org/project/lfreleng-test-python-project)
<!-- prettier-ignore-end -->

Example project used for testing Github actions that work with Python code.

Project name: lfreleng-test-python-project

## test-python-project

<!-- markdownlint-disable MD013 -->
Contains a sample Python project implementing a CLI tool with [Typer](https://typer.tiangolo.com/).
<!-- markdownlint-enable MD013 -->

<!--
# The section below renders the badges displayed at the top of the page
-->

##  Notes

Steps required to initialise pyproject.toml and create initial lock file:

```console
pdm init
pdm add -dG test pytest
pdm add -dG test coverage
pdm add -dG tox tox-pdm tox
pdm add -dG lint pre-commit
pdm add -dG docs sphinx
pdm add -dG docs sphinx-copybutton
pdm build
pdm install --dev
```

[pre-commit.ci results page]: https://results.pre-commit.ci/latest/github/lfreleng-actions/test-python-project/main
[pre-commit.ci status badge]: https://results.pre-commit.ci/badge/github/lfreleng-actions/test-python-project/main.svg
