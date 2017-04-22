## Assignment-5
### Distributed Optimizer

### [Assignment Link](http://cs.nyu.edu/courses/spring17/CSCI-GA.3033-006/assignment5.html)

### Platforms used:
* Python (version > 3.5)
* Tornado (version > 4.4.1)
* Cloudpickle (version > 0.2.2)
* Gensim (version > 1.0.1) (For word2vec modeling and optimization)

### How to run:
~~~~
cd /path/to/sea-assignments/assignment5

#Partition the dataset
python reformatter.py 'data/info_ret.xml' --num_partitions=5 --job_path='w2v_jobs'

#Run the gradient workers
python -m gradient

#Starts the optimizer coordinator
python -m coordinator --app='apps.word2vec' --job_path='w2v_jobs' --iterations 50
~~~~

### Check results:
~~~~
#In a python terminal

>>> import pickle
>>> m = pickle.load(open('w2v_jobs/0.out', 'rb'))
>>> m.most_similar(positive=['android', 'apple'], negative=['google'])[0]
('ios', 0.793526291847229)
~~~~