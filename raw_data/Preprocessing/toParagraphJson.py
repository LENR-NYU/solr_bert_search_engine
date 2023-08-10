import os
import json

input_folder = '/Users/yw511/Desktop/LENR_solr_react/data'  # Update with the actual path
output_folder = '/Users/yw511/Desktop/LENR_solr_react/data_paragraph'   # Update with the desired output path

for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        index = data['index']
        txt_content = data['text_content']
        
        jsonl_data = []
        for paragraph_number, paragraph in enumerate(txt_content, start=1):
            paragraph_index = f'{index}_{paragraph_number}'
            article_index = index
            
            paragraph_data = {
                'paragraph_index': paragraph_index,
                'article_index': article_index,
                'document_link': data['document_link'],
                'abstract': data['abstract'],
                'all_authors': data['all_authors'],
                'pdf_path': data['pdf_path'],
                'title': data['title'],
                'publisher': data['publisher'],
                'year_published': data['year_published'],
                'volume': data['volume'],
                'date_uploaded': data['date_uploaded'],
                'keywords': data['keywords'],
                'paragraph': paragraph,
            }
            
            jsonl_data.append(paragraph_data)
        
        jsonl_filename = os.path.splitext(filename)[0] + '.jsonl'
        jsonl_path = os.path.join(output_folder, jsonl_filename)
        
        with open(jsonl_path, 'w', encoding='utf-8') as jsonl_file:
            for item in jsonl_data:
                json.dump(item, jsonl_file)
                jsonl_file.write('\n')