# Beaker-py

A lightweight pure-Python client for Beaker.

## Installing

### Installing with `pip`

**beaker-py** is available [on PyPI](https://pypi.org/project/beaker-py/). Just run

```bash
pip install beaker-py
```

### Installing from source

To install **beaker-py** from source, first clone [the repository](https://github.com/allenai/beaker-py):

```bash
git clone https://github.com/allenai/beaker.git
cd beaker/bindings/python
```

Then run:

```bash
make dev-install
```

## Quick start

If you've already configured the [Beaker command-line client](https://github.com/allenai/beaker/), **beaker-py** will 
find and use the existing configuration file (usually located at `$HOME/.beaker/config.yml`).
Otherwise just set the environment variable `BEAKER_TOKEN` to your Beaker [user token](https://beaker.org/user).

Either way, you should then instantiate the Beaker client with `.from_env()`:

```python
from beaker import Beaker

beaker = Beaker.from_env(default_workspace="my_org/my_workspace")
```
