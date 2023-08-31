import os
import csv
import json
import pandas as pd

def preccess_txt(txt):
    sections = txt.strip().split('\n\n\n')
    results = []
    for section in sections:
        content = ''
        paragraphs = section.strip().split('\n\n')
        section_name = paragraphs[0]
        if "reference" in section_name.lower():
            continue
        paragraphs = paragraphs[1:]
        for paragraph in paragraphs:
            lines = paragraph.strip().split('\n')
            content = ' '.join(lines)
        results.append(content)
    return results

def process_txt_files(input_folder, csv_file, output_folder):
    df = pd.read_csv(csv_file)

    df.drop(columns=['Unnamed: 0', 'cleaned', 'images', 'tables', 'start', 'end'], inplace=True)
    print(df.columns)
    print(df.head())
    
    # Process each TXT file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            index = int(os.path.splitext(filename)[0])
            print("Process index ", index)
            if index in df['index'].values:
                print("Processing")
                txt_path = os.path.join(input_folder, filename)
                with open(txt_path, 'r', encoding='utf-8') as txt_file:
                    txt_content = txt_file.read()
                row = df.loc[index]

                txt_content = preccess_txt(txt_content)

                data = {
                    'index': index,
                    'document_link': str(row['document_link']) if not pd.isna(row['document_link']) else '',
                    'abstract': str(row['abstract']) if not pd.isna(row['abstract']) else '',
                    'all_authors': str(row['all_authors']).split('; ') if not pd.isna(row['all_authors']) else [],
                    'pdf_path': str(row['pdf_path']) if not pd.isna(row['pdf_path']) else '',
                    'title': str(row['title']) if not pd.isna(row['title']) else '',
                    'publisher': str(row['publisher']) if not pd.isna(row['publisher']) else '',
                    'year_published': str(row['year_published']) if not pd.isna(row['year_published']) else '',
                    'volume': str(row['volume']) if not pd.isna(row['volume']) else '',
                    'date_uploaded': str(row['date_uploaded']) if not pd.isna(row['date_uploaded']) else '',
                    'keywords': str(row['keywords']).split(', ') if not pd.isna(row['keywords']) else [],
                    'text_content': txt_content 
                }

                
                json_path = os.path.join(output_folder, f'{index}.json')
                with open(json_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)
                print("Processed")
                

# Example usage
input_folder = '/Users/yw511/Desktop/LENR_solr_react/raw_data/clean_paragraphs'
csv_file = '/Users/yw511/Desktop/LENR_solr_react/raw_data/literature-records_with_pdf - literature-records_with_pdf.csv'
output_folder = '/Users/yw511/Desktop/LENR_solr_react/data'

process_txt_files(input_folder, csv_file, output_folder)
