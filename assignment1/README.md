## Assignment-1
### Simple Load Balancer

### [Assignment Link](http://cs.nyu.edu/courses/spring17/CSCI-GA.3033-006/assignment1.html)

### Platforms used:
* Python (version > 3.5)
* [Tornado](http://www.tornadoweb.org/en/stable/)

### File Description: 
* Note: Ports are randomly calculated using the current username's md5 hash
* server\_single.py: Just starts a simple Hello World server at a random port
* server\_multiple.py: Starts three servers which output their own hostname when called.
* load\_balancer.py: Forwards requests to the three servers started by server\_multiple.py in an asynchronous way.
* start.py: Final assignment script, using code from the above scripts to start the load balancer and three backend servers in a single processe.

### How to run
python start.py
