from pyserini.search import FaissSearcher

import pandas as pd
import csv
import os

indexes_path = '/Users/yw511/Desktop/LENR_solr_react/index_paragraph_anserini'
searcher = FaissSearcher(indexes_path,
                         'facebook/dpr-question_encoder-multiset-base')

query = 'What is excess heat?'
hits = searcher.search(query, 20)

for i in range(len(hits)):
    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')