# GiA Core

GiA Core is a Python module containing much of the core functionality utilized by the various tasks managed by the GiA aggregation orchestration environment. However, this module is also in use in other environments such as in Jupyter Notebooks.

## Installation

```bash
pip install https://github.com/glaciers-in-archives/gia-core/archive/0.1.0.tar.gz
```

Note: You will need to install the dependencies manually.

## High-level modules in GiA Core

* datamodel
     - Contains the core classes and writers for the GiA RDF data model.
* labelstudio
     - Contains functions to write data files and templates for Label Studio.
* notebook
     - Contains helper functions for Jupyter Notebooks.
* repositories
     - Various API wrappers and scrapers for repositories or other aggregators (to be deprecated).
* service
     - Various integrations with APIs used internally, such as AWS S3 compatible services and the SPARQL Graph Store HTTP Protocol.
* wikidata
     - Various Wikidata helper functions.
