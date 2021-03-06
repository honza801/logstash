#!/usr/bin/python

# Deletes data from logstash older than 40 days

import os.path
from elasticsearch import Elasticsearch
import re
from datetime import date, datetime, timedelta
import logging

log_filename = '/var/log/'+os.path.basename(__file__)+'.log'
logging.basicConfig(format='%(asctime)s %(message)s', filename=log_filename, level=logging.INFO)

es = Elasticsearch()
logstash_pattern = re.compile('logstash-(\d+\.\d+\.\d+)')
max_date = date.today()-timedelta(days=40)
logging.info('max_date: %s' % max_date)

for line in es.cat.indices().split('\n'):
    m = logstash_pattern.search(line)
    if m == None: continue
    index = m.group(0)
    index_date = m.group(1)
    if datetime.strptime(index_date, '%Y.%m.%d').date() < max_date:
        logging.info("Deleting %s" % index)
        es.indices.delete(index=index)

