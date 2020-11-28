# Tb2UD

Convert Ancient Greek treebanks in the main formats supported by [Arethusa]() 
and [Perseids]() to UD. At the moment, it is designed to work with the treebanks 
compatible with:

* Perseus AGLDT
* [Daphne](https://perseids-publications.github.io/daphne-trees/)
* [Pedalion](https://github.com/perseids-publications/pedalion-trees/)

## Requirements

* Python 3.6+
* the package `udapy-python`, with some additional scripts to work with the formats 
of Perseus AGLDT; you must use the `agdt` branch in [my fork](https://github.com/francescomambrini/udapi-python) 
of that project, which already includes all the modules to work with those files.

*NEW*: The `agdt` branch of `udapi` should be automatically installed if you install 
everything from the `requirements.txt` (see below on how to set up a virtual environment).

**Important**: don't forget to add 2 folders to your `$PYTHONPATH`: `tb2UD` and 
`tb2UD/tb2ud`; for instance, you can do that by:

```bash
cd /path/to/tb2UD/
export PYTHONPATH="$(pwd):$(pwd)/tb2ud/"
```
Or, even better, create and configure a 
[virtual environment](https://docs.python.org/3.6/tutorial/venv.html) 
(see next paragraph).

## How to set up a `virtualenv`

If you don't know what a virtual environment is, you'll find a lot of good tutorials 
online, starting with [this one](https://docs.python.org/3.6/tutorial/venv.html). 
You may also want to consider [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/), 
which makes a lot of things easier to manage.

Follow these three steps:

1. create and activate a virtual environment (Python 3.6+); see the link above, if you don't 
know how do it.

2. install the required packages:

```bash
pip install -r requirements.txt 
```

3. create a `pth` file and enter the full path to the `tb2UD` and
`tb2UD/tb2ud` folders; see [here](https://stackoverflow.com/a/10739838).

If you have [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/), you also 
have a `add2virtualenv` script, which takes care of step 3 for you:

```bash
add2virtualenv directory1 directory2 ...
```

## How to use it

In the `scripts` folders, you'll find a few bash scripts to perform 
some of the most frequently used commands.

You can test that everything is working fine by running the following script:

```bash
# test.sh <input-file.xml>
cd test # go to the tb2ud/test folder
./test.sh data/hdt-1-20-39-bu2.xml 
```

(note that the script attempts to read an AGLDT XML file; it fails if the 
appropriate `udapi` blocks are not found)

If all goes well, you'll see a series of log entries, followed by the good old 
`Hello, World!` string.
