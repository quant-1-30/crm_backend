#! /bin/bash

set +e # warning continue
# poetry shell # interactive env
cd crm_backend && poetry run python main.py
