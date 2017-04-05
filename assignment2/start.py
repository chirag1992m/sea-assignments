# -*- coding: UTF-8 -*-
'''
Name: Chirag Maheshwari
Course: Search Engine Architecture

main script to load all the servers
'''

from assignment2 import front_end_server, indexer, index_server, document_server

import tornado.ioloop as iol

#Run the indexer first
indexer.run_indexer()

#Run the document server
document_server.run_document_servers()

#Run the index server
index_server.run_index_servers()

#Run the fron end server
front_end_server.run_front_end()

# Run the IO listen loop!
iol.IOLoop.current().start()