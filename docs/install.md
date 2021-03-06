---
layout: default
title: Installation
pdf: true
permalink: /install
toc: false
---

# Installation Local

To install from the Github repository:

```
git clone https://www.github.com/singularityhub/sregistry-cli.git
cd sregistry-cli
python setup.py install
```

We recommend for the latest features to use the development branch:

```
git clone -b development https://www.github.com/singularityhub/sregistry-cli.git
cd sregistry-cli
python setup.py install
```

Given that the current endpoints are limited, you will do ok with the above 
method. However, when the time comes to install specific modules, you would do
that by specifying the ones you want, e.g.,

```
pip install -e .[myclient]
```

To install from pip (granted that @vsoch has updated, this is likely only for
major versions, and it's usually best during development to install from the 
repository).

```
pip install sregistry
```

or for a particular extra client:

```
pip install sregistry[myclient]
```

For now, it's probably fastest and easiest to use the Singularity image.

# Singularity
To build a singularity container

```
sudo singularity build sregistry-cli Singularity
```

And now anywhere in these pages where you run an sregistry command, instead just
reference the image:

```
./sregistry-cli
```

and to activate a particular client endpoint, thanks to the [Standard Container Integration Format](https://containersftw.github.io/SCI-F/)
you can just use an `--app` flag instead:

```
singularity run --app registry sregistry-cli
```

I (@vsoch) expect to be improving these docs (asciinemas!) and adding additional endpoints soon!
