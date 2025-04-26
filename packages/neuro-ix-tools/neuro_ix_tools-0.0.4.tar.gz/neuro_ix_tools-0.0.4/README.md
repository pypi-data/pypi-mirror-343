# Neuro-iX Tools
Common Tools for Neuro-iX lab

## Getting started

### Install

You will need an environment with at least python 3.11 and run :

```
pip install neuro-ix-tool
```

Otherwise, you can clone the repository and use :

```
python cli.py
```

instead of `neuro-ix`.

### Setup

If you are using the package, you can just run :

```
neuro-ix init
```

which provide sane defaults for Narval. The configuration file is stored in your `.config` folder.

If you are using the repository, we advise you to use a local `.env` file by using the template available in `.example.env`.

### Usage

Inside this envrionment you have access to the `neuro-ix` command exposing one principal tool (for now).

#### FreeSurfer recon-all on SLURM cluster

For the usage of Neuro-iX, we defined a pipeline simplifying the usage of FreeSurfer for the Narval SLURM cluster. The main command is 

```
neuro-ix freesurfer recon-all
```
It allows the user to process all subject in either a BIDS or CAPS (Clinica) with FreeSurfer using one SLURM job per subjects.

which accepts the following arguments :
- `--bids-dataset` to specify the path to the root of a BIDS compliant dataset
- `--clinica-dataset` to specify the path to the root of a Clinica compliant dataset (CAPS)
- `--cortical-stats` a flag to only store the FreeSurfer's stats files 
- `--start-from` used in case there is more than 1000 subjects because of Narval jobs limit. It allows the user to determine at which subject index he wants to restart the command.

Example :

```
neuro-ix freesurfer recon-all --bids-dataset /path/to/dataset
```

And if the dataset include 1500 subjects, you will need to run, once all jobs are finished :

```
neuro-ix freesurfer recon-all --bids-dataset /path/to/dataset --start-from 1000
```

### Library

As a library, the `neuro_ix` package exposes :
- Classes to interact and query both BIDS and CAPS datasets for T1w MRIs
- Extendqble command classes 

## Contribute
### Setup

Once cloned, to get all necessary developement packages, you have to run :
```
pip install -r dev_requirements.txt
```

### Tests

#### Test tools

We use pytest for our unit tests and pytest-cov for coverage. You can easily run them in VSCode or with the following commands :

```
pytest --cov
```

We use ruff for linting and formating, which is automatically applied with `precommit`.
We also use `ssort`, `pydocstyle`, `mypy` and `pylint` to assure consistent code quality.

#### Test data

All test data are extracted from MR-ART :

>Nárai, Á., Hermann, P., Auer, T. et al. Movement-related artefacts (MR-ART) dataset of matched motion-corrupted and clean structural MRI brain scans. Sci Data 9, 630 (2022). https://doi.org/10.1038/s41597-022-01694-8
