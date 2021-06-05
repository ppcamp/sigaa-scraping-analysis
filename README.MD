# Student's competency analisis: An graph approach

This repository contains some codes used in the article that will be published later.

---

- [Student's competency analisis: An graph approach](#students-competency-analisis-an-graph-approach)
  - [How it works?](#how-it-works)
  - [How to run](#how-to-run)
  - [Documentation](#documentation)
    - [How to document](#how-to-document)
    - [Sphinx themes:](#sphinx-themes)
  - [Some usefull commands:](#some-usefull-commands)
  - [Packages needed](#packages-needed)
    - [See also](#see-also)

----

## How it works?

This code uses the following approach:

<p align="center">
  <img
    src="src/doc/source/_static/img/logo.png"
    width="200px"
    alt="Image #1"/>
</p>

## How to run

The project was created and designed under "jupyter researchers" approach. Doing so, you'll need an jupyter
interface to open it.

> You can install jupyter using:
> `pip install jupyterlab`

## Documentation

The [documentation](src/doc/build/html/index.html) of `modules` is inside `src/doc/build/html` folder.


### How to document

The project was developed using *Google Docstrings* and *RST (Reestructured text)* guides.
You can check [here](https://www.google.com/search?q=google+documentation+python&oq=google+pydocumention+&aqs=chrome.1.69i57j0i13l9.8494j0j4&sourceid=chrome&ie=UTF-8) and
[here](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html).


### Sphinx themes:
- furo (black)
- read the docs (default)
- asteroid

## Some usefull commands:

```bash
# run all the tests
python src/tests.py

# autodocumentation sphinx api (inside source folder)
sphinx-apidoc -o . ../../modules/

# generate html pages for sphinx
make html

# create a new documentation
sphinx-quickstart
```

> [Why don't use markdown to documentation](https://www.ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/)

## Packages needed

* To install the python packages, type (*inside src directory*):

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

### See also

> To install other themes you must search for a python package equivalent for that theme.

- [Doc sphinx](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html)

- https://sphinx-themes.org/
- https://stackoverflow.com/questions/13516404/sphinx-error-unknown-directive-type-automodule-or-autoclass
- https://www.youtube.com/watch?v=b4iFyrLQQh4&ab_channel=avcourt
- https://stackoverflow.com/questions/34533346/incorrect-cross-reference-syntax-gives-confusing-undefined-label-warning
- https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-pygments_style