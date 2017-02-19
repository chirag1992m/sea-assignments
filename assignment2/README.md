# Assignment-2
## Index and Retrieval

### [Assignment Link](http://cs.nyu.edu/courses/spring17/CSCI-GA.3033-006/assignment2.html)

### Platforms used:
* Python (version > 3.5)
* [Tornado](http://www.tornadoweb.org/en/stable/)

## Checkpoint 1 - Front End Server

* Create Inventory Module of Index and Document Servers
* Gets the query
* Forward the query to Index Servers
* Parse and sort the result
* Get the document snippets for the results
* Pack it in a JSON and reply

* Index Server Links (Already Running by Professor): [1](http://linserv2.cims.nyu.edu:35315/index?q=personalized), [2](http://linserv2.cims.nyu.edu:35316/index?q=personalized), [3](http://linserv2.cims.nyu.edu:35317/index?q=personalized)
* Document Server Links (Already Running by Professor): [1](http://linserv2.cims.nyu.edu:35318/doc?id=414&q=personalized), [2](http://linserv2.cims.nyu.edu:35319/doc?id=709&q=personalized), [3](http://linserv2.cims.nyu.edu:35320/doc?id=674&q=personalized)

**To run**: python front\_end\_server.py

## Checkpoint 2 - Indexer

* Reads the wiki_dataset.xml file
* Creates inverted indexes for the index servers partitioned across document
* Creates document indexes for the document servers partitioned across document

**To run**: python indexer.py

## Checkpoint 3 - Index and Document Server

### Index server
* Starts an index server at the address /index
* Index server loads the inverted index into memory
* Given a query, they score all the document using dot product and then return the top 10 results in a JSON format

**To run**: python index\_server.py

### Document server
* Starts a document server at the address /doc
* Index server loads the document index into memory
* Given a query, returns the information of a specific document and a specific query

**To run**: python document\_server.py

## Checkpoint 4 - Start script

* Starts all the components in one go

**To run**: python start.py