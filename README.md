Figma Link:
https://www.figma.com/file/GPDbDmAzsXbCah9icDb45K/Google-search?type=design&node-id=0%3A1&mode=design&t=rdUopOaXUMz2RIh1-1

Search Engine Test Cases:
1. What is excess heat?
2. What is the current status of research on "cold fusion"?
3. What are the proposed mechanisms for "LENR" reactions?
4. How are "low energy nuclear reactions" applied in various fields?
5. What are the outcomes of experiments involving "palladium deuteride"?
6. What is the significance of "anomalous heat" in nuclear reactions?
7. What are the leading theories explaining "LENR" phenomena?
8. How is "excess heat" observed in certain nuclear reactions?
9. Can you explain the "Fleischmann Pons" experiment and its results?
10. How does "transmutation" occur in the context of "LENR"?
11. What role does "palladium loading" play in "cold fusion" experiments?
12. Are there successful attempts at "replicating" cold fusion?
13. What are the most notable "experimental results" in "LENR" research?
14. How do "nanoparticles" contribute to nuclear reactions in "LENR"?
15. What is the role of "hydrogen absorption" in palladium-based reactions?
16. How does "LENR" relate to power generation applications?
17. What are the existing "safety concerns" associated with "LENR"?
18. How is "deuterium gas loading" used in experimental setups?
19. What are the main "challenges" faced in "LENR" research?
20. How is "helium production" observed in "cold fusion" reactions?

11450 entries

Pyserini:
python -m pyserini.encode input \
  --corpus /Users/yw511/Desktop/LENR_solr_react/data_paragraph_anserini \
  --fields text \
  --shard-id 0 \
  --shard-num 1 \
output \
  --embeddings /Users/yw511/Desktop/LENR_solr_react/index_paragraph_anserini \
  --to-faiss \
encoder \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --fields text \
  --batch 32 \
  --device cpu

1. Start Front-end
npm start run

2. Start Back-end
conda activate LENR1
flask --app app.py --debug run

3. Start Solr
export solr_home=/Users/yw511/Solr/solr-9.2.1
cd $solr_home
bin/solr start -p 8983

filter fields: all_authors, publisher, year_published

References:
https://www.youtube.com/watch?v=NDbruK1fzG8&t=2434s
https://github.com/adrianhajdin/project_google_clone
https://github.com/django-haystack/pysolr
https://github.com/castorini/pyserini/blob/master/docs/usage-index.md#building-a-bm25-index-embeddable-python-implementation