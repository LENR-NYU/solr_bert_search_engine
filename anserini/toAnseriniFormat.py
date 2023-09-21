
import json
from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np

class FaissVectorizer:

    def __init__(self, ids, paragraphs):
        # self.encoder = SentenceTransformer("castorini/tct_colbert-v2-hnp-msmarco")
        self.ids = ids
        self.paragraphs = paragraphs
        self.sentence_embeddings = None
        self.index = None
        self.encoder = SentenceTransformer("bert-base-nli-mean-tokens")

    def add_paragraphs(self, paragraphs):
        self.sentence_embeddings = self.encoder.encode(paragraphs)
        print("Shape of sentence_embeddings:", self.sentence_embeddings.shape)
        print("First few elements of sentence_embeddings:", self.sentence_embeddings[:5])
    
    def indexing(self):
        d = self.sentence_embeddings.shape[1]
        self.index = faiss.IndexFlatL2(d)
        self.index.add(self.sentence_embeddings)

        if self.index is not None:
            print("Shape of index:", self.index.ntotal, "x", self.index.d)
            # print("First few elements of index:")
            # for i in range(min(2, self.index.ntotal)):
            #     print(self.index.reconstruct(i))
        else:
            print("Index is not initialized yet.")

    def outputIndex(self, output_file):
        if self.index is not None:

            with open(output_file, "w") as jsonl_file:

                for i in range(self.index.ntotal):
                    vector = self.index.reconstruct(i).tolist()
                    entry = {"id": self.ids[i], "vector": vector}
                    json.dump(entry, jsonl_file)
                    jsonl_file.write('\n')
                    
            print("Index data (JSONL) written to", output_file)
        else:
            print("Index is not initialized yet.")



# jsonl_folder = '/Users/yw511/Desktop/LENR_solr_react/data_paragraph'
# output_file = '/Users/yw511/Desktop/LENR_solr_react/index_paragraph/index.jsonl'

# ids = []
# paragraphs = []

def load_jsonl_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".jsonl"):
            with open(os.path.join(folder_path, filename), "r") as file:
                lines = file.readlines()
                for line in lines:
                    json_data = json.loads(line)
                    paragraph = json_data.get("paragraph", "")
                    id = json_data.get("paragraph_index", "")
                    ids.append(id)
                    paragraphs.append(paragraph)

json_folder = '/Users/yw511/Desktop/LENR_solr_react/data_fulltext'
output_file = '/Users/yw511/Desktop/LENR_solr_react/index_fulltext/index.jsonl'

ids = []
fulltext = []

def load_json_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), "r") as file:
                json_data = json.load(file)  # Load the entire JSON file
                paragraph = json_data.get("paragraph", "")
                id = json_data.get("paragraph_index", "")
                ids.append(id)
                fulltext.append(paragraph)

load_json_files(json_folder)
print("Number of paragraphs:", len(fulltext))
print("Number of ids:", len(ids))

faiss_vectorizer = FaissVectorizer(ids, fulltext)
faiss_vectorizer.add_paragraphs(fulltext)
faiss_vectorizer.indexing()
faiss_vectorizer.outputIndex(output_file)

# load_jsonl_files(jsonl_folder)
# print("Numbers of paragraphs:", len(paragraphs))
# print("Numbers of ids:", len(ids))
# faiss_vectorizer = FaissVectorizer(ids, paragraphs)
# faiss_vectorizer.add_paragraphs(paragraphs)
# faiss_vectorizer.indexing()
# faiss_vectorizer.outputIndex(output_file)

# for idx in search_results:
#     print(f"Index: {idx}, Vector: {faiss_vectorizer.vectors[idx]}")
