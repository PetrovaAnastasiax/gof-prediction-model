# Overview

The goal of this repository is to train a code2vec model, using TensorFlow

## How to run

Start JuPyter Notebook server in Docker, it is one of the easiest ways to setup TensorFlow Jupyter environment

> docker-compose up .

Place the labeled classes in following directory `code2vec/JavaPatterns/`

Run JupyterNotebook cells to train code2vec model and create Polynomial classifier, which is used in [gof-pattern-prediction-server](https://github.com/PetrovaAnastasiax/gof-pattern-prediction-server)
