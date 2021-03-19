# Student's competency analisis: An graph approach

This repository contains some codes used in the article that will be published later.

---

- [Student's competency analisis: An graph approach](#students-competency-analisis-an-graph-approach)
  - [How to run](#how-to-run)
    - [Packages needed](#packages-needed)
    - [Running](#running)
    - [Sphinx themes:](#sphinx-themes)

----

## How to run

### Packages needed

* To install the python packages type (*inside src directory*)
```bash
python install -r requirements.txt
```
* Install the graphviz:

  You can install the graphviz by the package [site](https://graphviz.org/download/) or typing:
  * in debian-based linux:
  ```bash
  sudo apt install graphviz
  ```
  * or using a choco (windows)
  ```bash
  choco install graphviz
  ```


### Running
To run this code you must execute:
```bash
# Otherwise, it'll throw an error in windows
dot -c

python src/main.py
```


### Sphinx themes:
- furo (black)
- read the docs (default)
- asteroid

*See*: https://sphinx-themes.org/

> To install other themes you must search for a python package equivalent for that theme.