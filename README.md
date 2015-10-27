# The influence of natural selection, mating models & migration on the shape of the ancestry graph.

This is a 4th year project developed as a part of Joint Honours Computer Science and Mathematics degree at University of Glasgow.

# Installation and Usage

In order to run the simulation and create the graph you can execute `./project --generateGraph=<parameterFile>`. The graphs will be generated and written in data directory. This step doesn't have any dependencies required apart from python 2.7 or python 3.

To carry out some symbolic derivation of mathematical formulae used in this project you can execute `./project --derive`. This step has a dependency on the sage package, which can be installed, i.e. on modern Fedora by executing `dnf install sagemath` as root user. This dependency is optional and restricted to this particular command so as not to force any user to install sage as dependency in their system.

To unit test, execute `./project --test`

There is no mechanism for graph processing developed as of yet. Any dependencies (networkx, etc) will be installable via pip in virtualenv, that is `virtualenv venv` to create virtual environment and then `source venv/bin/activate` to activate virtualenv and then `pip install -r requirements.txt` to install all required dependencies.

