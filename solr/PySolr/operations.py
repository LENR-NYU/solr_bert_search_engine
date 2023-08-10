import pysolr
import json
import os

class SolrClient:
    def __init__(self, solr_url):
        self.solr = pysolr.Solr(solr_url)
    
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

solr_url = 'http://localhost:8983/solr/search_lenr_0'
jsonl_file = '/Users/yw511/Desktop/LENR/sample0.jsonl'
jsonl_folder = '/Users/yw511/Desktop/LENR_solr_react/data_paragraph'

solr_client = SolrClient(solr_url)
# solr_client.inject_data_from_jsonl(jsonl_file)
# solr_client.delete_all_documents()
solr_client.inject_data_from_folder(jsonl_folder)
