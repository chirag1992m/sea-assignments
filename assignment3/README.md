## Assignment-3
### MapReduce Framework

### [Assignment Link](http://cs.nyu.edu/courses/spring17/CSCI-GA.3033-006/assignment3.html)

### Platforms used:
* Python (version > 3.5)
* Tornado (version > 4.4.1)

### Description:
This assignment aims to build a Map-Reduce Framework with an interface that is largely based on [Hadoop's Streaming Interface](https://hadoop.apache.org/docs/stable/hadoop-streaming/HadoopStreaming.html). It contains three main components as desribed below:
1. **inventory**: A static file containing the constants used by the framework. For eg, the number of workers used and their locations.
2. **coordinator**: Master server/script that coordinates the work between the different components (Mappers and Reducers)
3. **workers**: worker acting as a mapper or reducer depending upon the request received. It uses components/classes defined in **reducer** and **mapper**.

## How to use
Define an application in form of map-reduce and put it in one directory with the parent directory common with the above components. For eg: wordcount/mapper.py and wordcount/reducer.py. We'll refer to these paths as ``mapper_path`` and ``reducer_path``. Now, put the input files in a directory named as <counter>.in where <counter> goes from ``0`` to ``N`` depending upon how many mappers you want to use. Each file will be inputted to a different mapper. Keep these files in a directory with the parent directory common to the components. We'll call this directory as ``job_path``.

After all this is completed, start the workers using the command:
```
python workers.py
```

After running the workers, start the master coordinator to actually do the work using these workers:
```
python coordinatory.py --mapper_path=<mapper_path> --reducer_path=<reducer_path> --job_path=<job_path> --num_reducers=<Number of reducers>
```

**PS**: To increase/decrease the number of workers, change the constant ``NUM_WORKERS`` inside inventory.py accordingly.