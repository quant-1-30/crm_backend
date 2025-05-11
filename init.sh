#! /bin/bash

# set +e # warning continue

# initialize database
python init.py

# activte web
cd crm_backend && poetry run python main.py
