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

- **Fast job submission**: Submit one or multiple observables to Cortex with a different set of analysers
- **Bulk submission**: Submit jobs to Cortex observables from a text file
- **Extract artifacts**: Submit one or multiple job and display only the extracted artifacts
- **Download files**: Download extracted files from the job artifacts
- **Use aliases for analysers**: Map your own aliases to launch your favorite analysers
- **Multi instance config**: Submit jobs to another Cortex instance

[TheHive Project]: https://thehive-project.org/
[Cortex]: https://github.com/TheHive-Project/Cortex


## Installation

### with pip 

`corcli` is published as a [Python package] and can be installed with `pip`, ideally by using a [virtual environment]. Open up a terminal and install corcli with:

```sh
pip install corcli
```

[Python package]: https://pypi.org/project/corcli/
[virtual environment]: https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment

### using Docker

A [docker image] is available from the repository and comes with all dependencies pre-installed. Open up a terminal and pull the image with:

TODO.

[docker image]: https://pypi.org/project/corcli/

## License

GPLv3