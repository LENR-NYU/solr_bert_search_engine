import pysolr
import json
import os
import requests
# from sentence_transformers import SentenceTransformer
from _dprEncoder import DprQueryEncoder
import faiss

class SolrClient:
    def __init__(self, solr_url):
        self.solr = pysolr.Solr(solr_url)
        # self.encoder = SentenceTransformer("bert-base-nli-mean-tokens")
        self.encoder = DprQueryEncoder('/Users/yw511/Desktop/LENR_solr_react/dpr-question_encoder-multiset-base')
    
    def inject_data_from_jsonl(self, jsonl_file):
        # Open the JSONL file
        with open(jsonl_file, 'r') as file:
            for line in file:
                data = json.loads(line)
                self.solr.add([data])
        self.solr.commit()

    def inject_data_from_folder(self, jsonl_folder):
        for filename in os.listdir(jsonl_folder):
            if filename.endswith('.jsonl'):
                jsonl_path = os.path.join(jsonl_folder, filename)
        
                with open(jsonl_path, 'r', encoding='utf-8') as jsonl_file:
                    for line in jsonl_file:
                        item = json.loads(line)
                        print("Loading index", item['article_index'])
                        self.solr.add([item])
        self.solr.commit()

    def delete_all_documents(self):
        self.solr.delete(q='*:*')
        self.solr.commit()

    def modify_solr_schema(self, solr_url, field_name, new_field_type):
    # Define the new field type
        field_definition = {
            "replace-field-type": {
                "name": field_name,
                "class": new_field_type
            }
        }

        response = requests.post(f"{solr_url}/schema", json=field_definition)

        if response.status_code == 200:
            print(f"Schema modification successful for field '{field_name}'")
        else:
            print(f"Schema modification failed: {response.status_code} - {response.text}")

    def inject_index(self, jsonl_folder):

        for filename in os.listdir(jsonl_folder):
            if filename.endswith('.jsonl'):
                jsonl_path = os.path.join(jsonl_folder, filename)
        
                with open(jsonl_path, 'r', encoding='utf-8') as jsonl_file:
                    for line in jsonl_file:
                        item = json.loads(line)
                        paragraph_index = item['id']
                        vector = item['vector']
                        formatted_vector = [float(v) for v in vector]

                        results = self.solr.search('paragraph_index:"{}"'.format(paragraph_index))
                        if results:
                            doc_id = results.docs[0]['id']
                            existing_doc = results.docs[0]
                            update_doc = {
                                'vector': formatted_vector
                            }
                            update_doc.update(existing_doc)
                            self.solr.add([update_doc])
        self.solr.commit()
        print("Vectors updated in Solr")
    
    def search_with_query(self, query):

        # sentence_embedding = self.encoder.encode([query])
        # print(sentence_embedding.shape)
        # d = sentence_embedding.shape[1]
        # index = faiss.IndexFlatL2(d)
        # index.add(sentence_embedding)
        # search_list = index.reconstruct(0).tolist()
        # print(len(search_list))

        sentence_embedding = self.encoder.encode(query)
        sentence_embedding = sentence_embedding.reshape((1, len(sentence_embedding)))
        d = sentence_embedding.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(sentence_embedding)
        search_list = index.reconstruct(0).tolist()
        # print(len(search_list))

        # print("Encoded Query:", search_list)
        knn_query = '{!knn f=vector topK=15}' + str(search_list)
        # print(knn_query)
        results = self.solr.search(q=knn_query, rows=15)
        print(len(results))
        for r in results:
            print(r['paragraph'][0])
        for r in results:
            print(r['paragraph_index'][0])


solr_url = 'http://localhost:8983/solr/search_lenr_0'
solr_url_1 = 'http://localhost:8983/solr/search_lenr_1'
# jsonl_file = '/Users/yw511/Desktop/LENR/sample0.jsonl'
jsonl_folder = '/Users/yw511/Desktop/LENR_solr_react/data_fulltext'
index_jsonl_folder = '/Users/yw511/Desktop/LENR_solr_react/index_paragraph'

solr_client = SolrClient(solr_url_1)
# solr_client.inject_data_from_jsonl(jsonl_file)
# solr_client.delete_all_documents()
solr_client.inject_data_from_folder(jsonl_folder)
# solr_client.inject_index(index_jsonl_folder)
# solr_client.search_with_query("What is excess heat")

# field_name = "volume"
# new_field_type = "string"
# solr_client.modify_solr_schema(solr_url, field_name, new_field_type)
