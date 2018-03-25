Alpheios Translation Service
===

[![Build Status](https://travis-ci.org/alpheios-project/alpheios-translation-service.svg?branch=master)](https://travis-ci.org/alpheios-project/alpheios-translation-service)
[![Coverage Status](https://coveralls.io/repos/github/alpheios-project/alpheios-translation-service/badge.svg?branch=master)](https://coveralls.io/github/alpheios-project/alpheios-translation-service?branch=master)


Web Service that provides translations for lemmas

## Development

### Installation

Create virtual env for python 3 and run following commands

```shell
python scripts.py db-create
python scripts.py data-download
python scripts.py data-ingest
```

### Run

```shell
# Run a quick demo
python run.py
```

### Structure

- The whole project revolve around the Corpus objects (`atservices.corpora.base.Corpus`). 
    - Ingesting new data with new input format should be dealt with the creation of new Corpus subclasses, such as
    `atservices.corpora.collatinus.CollatinusCorpus`
    - Data that did not match the database knowledge base are stored in a Miss table for which we offer a cleaning system.
- Errors are handled by a specific Error Handler and specific classes written in `atservices.error`
- Each language service should have its own blueprint as they might differ in the corpus/corpora system they use.
For an example, look at `atservices.main.latin` for the full blueprint and `atservices.create_app` for the generation
    - A generic response creation service to produce JSON is available at `atservices.utils`.
- Scripts such as scripts for ingestion should be written in `atservices.scripts`
    - Scripts are divided into three types : 
        - database helpers (building, creating, dropping database) : `atservices.scripts.make_db_cli()`
        - ingestion helpers (ingesting, downloading, recreating data) : `atservices.scripts.make_data_cli()`.
            - Corpus specific functions are called from within this CLI. You should write your own corpus specific function
            in `atservices.scripts.collatinus`-likes modules
        - data and usage survey : `atservices.scripts.make_data_survey_cli()`
        
### Tests 

To come

## Running on production

1. To run on production, the same installation bases are valid : create a virtual env, install dependencies from requirements.txt.
2. You should also produce a Production Specific config object such as the ones available at `atservices.config`
3. Finally, create a python file such as `run.py` that will be running the app through `atservices.create_app` with 
your environment specific configuration