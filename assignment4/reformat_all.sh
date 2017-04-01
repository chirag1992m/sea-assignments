#!/bin/bash

# This is just a template that demonstrates how you might set up your project. Feel free to edit this file.

python -m assignment4.reformatter assignment2/data/info_ret.xml --job_path=assignment4/idf_jobs/ --num_partitions=1
python -m assignment4.reformatter assignment2/data/info_ret.xml --job_path=assignment4/docs_jobs/ --num_partitions=3
python -m assignment4.reformatter assignment2/data/info_ret.xml --job_path=assignment4/invindex_jobs/ --num_partitions=3

python -m assignment3.workers
python -m assignment3.coordinator --mapper_path=assignment4/mr_apps/invindex_mapper.py --reducer_path=assignment4/mr_apps/invindex_reducer.py --job_path=assignment4/invindex_jobs --num_reducers=3
python -m assignment3.coordinator --mapper_path=assignment4/mr_apps/docs_mapper.py --reducer_path=assignment4/mr_apps/docs_reducer.py --job_path=assignment4/docs_jobs --num_reducers=3
python -m assignment3.coordinator --mapper_path=assignment4/mr_apps/idf_mapper.py --reducer_path=assignment4/mr_apps/idf_reducer.py --job_path=assignment4/idf_jobs --num_reducers=1 --timeout=60
