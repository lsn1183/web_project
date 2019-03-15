#!/bin/sh
homepath=/home/pset
export PYTHONPATH=$homepath/CI_Script/lgatio:$homepath/Spec2DB
lsof -i:5000 | grep python | awk '{print$2}' | xargs kill -9
rm -rf APScheduler.lock
python spec_server_if.py
