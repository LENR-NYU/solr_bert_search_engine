from flask import Flask, request, jsonify
from flask_cors import CORS
# from sentence_transformers import SentenceTransformer
from _dprEncoder import DprQueryEncoder
import faiss
import requests
import json

import bert
import pandas as pd

app = Flask(__name__)
CORS(app)
encoder = DprQueryEncoder('/Users/yw511/Desktop/LENR_solr_react/dpr-question_encoder-multiset-base')
solr_url = 'http://localhost:8983/solr/search_lenr_0/select'

model = bert.QA('model')

def search_with_query(query, rows):

    ## Process query for dense vector search
    sentence_embedding = encoder.encode(query)
    sentence_embedding = sentence_embedding.reshape((1, len(sentence_embedding)))
    d = sentence_embedding.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(sentence_embedding)
    search_list = index.reconstruct(0).tolist()
    knn_query = '{!knn f=vector topK='+str(rows)+'}' + str(search_list)
    
    ## Ready for solr request
    session = requests.Session()
    session.stream = False
    session.verify = True
    requests_method = getattr(session, 'get')
    url = 'http://localhost:8983/solr/search_lenr_0/select'
    response = requests_method(url, data={'q': knn_query, 
                                          'rows':rows,
                                          'facet':'true',
                                          'facet.field':['all_authors','publisher','year_published']})
    # response = requests.get(solr_url, params={'q': knn_query, 'rows':limit})

    if response.status_code == 200:
        try:
            # Try to parse the JSON response
            return response.json()
        except json.JSONDecodeError:
            # Handle the case where the response is not valid JSON
            return {"error": "Invalid JSON response from Solr"}
    else:
        # Handle HTTP errors, e.g., not found, server error, etc.
        return {"error": f"HTTP error: {response.status_code}"}
    
def qa_with_query(doc, query):
    # print("doc", doc)
    # print("query", query)
    answer = model.predict(doc, query)
    return answer

@app.route("/search")
def search():
    query = request.args.get('q', default = '', type = str)
    rows = request.args.get('rows', default = 100, type = int)
    results = search_with_query(query, rows)
    return results

@app.route("/qa")
def qa():
    query = request.args.get('q', default = '', type = str)
    doc = request.args.get('doc', default = '', type = str)
    results = qa_with_query(doc, query)
    return results