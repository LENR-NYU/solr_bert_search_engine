import pysolr
import json
import os
import requests
from sentence_transformers import SentenceTransformer
import faiss

class SolrClient:
    def __init__(self, solr_url):
        self.solr = pysolr.Solr(solr_url)
        self.encoder = SentenceTransformer("bert-base-nli-mean-tokens")
    
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
        sentence_embedding = self.encoder.encode([query])
        # print(sentence_embedding.shape)
        d = sentence_embedding.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(sentence_embedding)
        search_list = index.reconstruct(0).tolist()
        # print("Encoded Query:", search_list)
        knn_query = '&q={!knn f=vector topK=5}' + str(search_list)
        results = self.solr.search(q='*:*',raw_query=knn_query)
        print(len(results))
        for r in results:
            print(r['paragraph'])


solr_url = 'http://localhost:8983/solr/search_lenr_0'
jsonl_file = '/Users/yw511/Desktop/LENR/sample0.jsonl'
jsonl_folder = '/Users/yw511/Desktop/LENR_solr_react/data_paragraph'
index_jsonl_folder = '/Users/yw511/Desktop/LENR_solr_react/index'

solr_client = SolrClient(solr_url)
# solr_client.inject_data_from_jsonl(jsonl_file)
# solr_client.delete_all_documents()
# solr_client.inject_data_from_folder(jsonl_folder)
# solr_client.inject_index(index_jsonl_folder)
solr_client.search_with_query("what is excess heat?")

# field_name = "volume"
# new_field_type = "string"
# solr_client.modify_solr_schema(solr_url, field_name, new_field_type)
