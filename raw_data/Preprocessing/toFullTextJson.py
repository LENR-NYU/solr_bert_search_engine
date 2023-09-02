import os
import json

input_folder = '/Users/yw511/Desktop/LENR_solr_react/data'  # Update with the actual path
output_folder = '/Users/yw511/Desktop/LENR_solr_react/data_fulltext'   # Update with the desired output path

for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        index = data['index']
        txt_content = data['text_content']
        
        jsonl_data = []

        article_index = index
        
        text_data = {
            'article_index': article_index,
            'document_link': data['document_link'],
            'abstract': data['abstract'],
            'all_authors': data['all_authors'],
            'title': data['title'],
            'publisher': data['publisher'],
            'year_published': data['year_published'],
            'volume': data['volume'],
            'date_uploaded': data['date_uploaded'],
            'keywords': data['keywords'],
            'fulltext': " ".join(txt_content),
        }
            
        jsonl_data.append(text_data)
        
        jsonl_filename = os.path.splitext(filename)[0] + '.json'
        jsonl_path = os.path.join(output_folder, jsonl_filename)
        
        with open(jsonl_path, 'w', encoding='utf-8') as jsonl_file:
            for item in jsonl_data:
                json.dump(item, jsonl_file)
                jsonl_file.write('\n')