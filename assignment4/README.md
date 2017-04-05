## Assignment-4
### Distributed Indexer

### [Assignment Link](http://cs.nyu.edu/courses/spring17/CSCI-GA.3033-006/assignment4.html)

### Platforms used:
* Python (version > 3.5)
* Tornado (version > 4.4.1)
* Map-Reduce Framework ([Assignment-3](../assignment3/README.md))
* Search-Engine Framework ([Assignment-2](../assignment2/README.md))

### File/Directory description:
* **docs\_jobs**: Job directory for Document Store Map-Reduce task (Task-1)
* **idf\_jobs**: Job directory for IDF score Map-Reduce task (Task-2)
* **invindex\_jobs**: Job directory for inverted index partitioned by document Map-Reduce task (Task-3)
* **mr\_apps**: Contains the mapper and reducer scripts for all the jobs
* **reformatter.py**: Partitions the dataset into given number of partitions by `document`
* **reformat\_all.sh**: Bash script to run reformatter for all the different tasks
* **start.py**: Runs the map-reduce programs using the coordinator in assignment-3 and moves the produced output to be used in assignment-2 search engine

### How to run:
~~~~
cd /path/to/sea-assignments/
./assignment4/reformat_all.sh
python -m assignment3.workers
#In a different terminal keeping the above workers running
python -m assignment4.start
#Now the workers can be killed off if not needed anymore

#Starts the search engine
python -m assignment2.start
~~~~
