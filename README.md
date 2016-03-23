# The influence of natural selection, mating models & migration on the shape of the ancestry graph.

This is a 4th year project developed as a part of Joint Honours Computer Science and Mathematics degree at University of Glasgow.

# Installation and Usage

In order to run a simulation batch and create all the graph files, compute Tmrca and run Mann-Whitney statistics you can execute `./project --runExperiments s2 mrca2 proc2`. The graphs will be generated and written in results directory. The step s2 does not have any dependencies required apart from Cpython 2.7, Cpython 3, pypi or jython. proc2 is dependent on the networkx package.

To carry out some symbolic derivation of mathematical formulae used in this project you can execute `./project --derive`. This step has a dependency on the sage package, which can be installed, e.g. on modern Fedora by executing `dnf install sagemath` as root user. This dependency is optional and restricted to this particular command so as not to force any user to install sage as dependency in their system.

To unit test, execute `./project --test`.

You can install all of dependencies described above using virtualenv in the following way:
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
