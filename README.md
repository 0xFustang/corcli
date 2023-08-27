# corcli - Cortex CLI client

[Cortex] is a Powerful Observable Analysis and Active Response Engine. While it is usually used along with [TheHive Project], why not using it on a daily basis in a CLI fashion.

`corcli` was built in Python for this specific purpose.

![Demo](img/demo.gif)

---

**Documentation:** https://0xfustang.github.io/corcli-docs/

**Source Code:** https://github.com/0xFustang/corcli

---

## Features

Key features are:

- **Fast job submission**: Submit one or multiple observables to Cortex with a different set of analyzers
- **Bulk submission**: Submit multiple observables from a text file
- **Extract artifacts**: Display only the extracted artifacts (.e.g IOCs)
- **Download files**: Download extraced files when available
- **Use aliases for analyzers**: Map your own aliases to launch your favorite analyzers
- **Define alias presets**: Define analysers presets that will call a group of analysers
- **Multi instance config**: Submit your jobs to another Cortex instance

[TheHive Project]: https://thehive-project.org/
[Cortex]: https://github.com/TheHive-Project/Cortex


## Installation

### with pip 

`corcli` is published as a [Python package] and can be installed with `pip`, ideally by using a [virtual environment]. Before installing `corcli`, install `libmagic` as [explained] in the installation doc.

Open up a terminal and install corcli with:

```sh
pip install corcli
```

[explained]: https://0xfustang.github.io/corcli-docs/getting-started/#with-pip-recommended
[Python package]: https://pypi.org/project/corcli/
[virtual environment]: https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment

### using Docker

A [docker image] is available from the repository and comes with all dependencies pre-installed. Open up a terminal and pull the image with:

```sh
docker pull ghcr.io/0xfustang/corcli:1.1.0
```

[docker image]: https://github.com/0xFustang/corcli/pkgs/container/corcli

## License

GPLv3