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
3. **workers**: worker acting as a mapper or reducer depending upon the request received.

