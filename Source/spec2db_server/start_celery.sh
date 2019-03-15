#!/bin/sh
homepath=/home/pset
export PYTHONPATH=$homepath/CI_Script/lgatio:$homepath/Spec2DB
celery worker -A spec_server_if.celery -Q export_task -E -l info -c 1
