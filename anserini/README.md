Anserini Encode:
__init__.py: import library
__main__.py
_aggretriever.py: AggretrieverDocumentEncoder, AggretrieverQueryEncoder
_ance.py: AnceEncoder, AnceDocumentEncoder, AnceQueryEncoder
_auto.py: AutoQueryEncoder, AutoDocumentEncoder
_base.py: DocumentEncoder, QueryEncoder, JsonlCollectionIterator, RepresentationWriter, FaissRepresentationWriter, JsonlRepresentationWriter, PcaEncoder
_cached_data.py: CachedDataQueryEncoder
_dpr.py: DprDocumentEncoder, DprQueryEncoder
_slim.py: SlimQueryEncoder
_splade.py: SpladeQueryEncoder
_tct_colbert.py: TctColBertDocumentEncoder, TctColBertQueryEncoder
_tok_freq.py: TokFreqQueryEncoder
_unicoil.py: UniCoilEncoder, UniCoilDocumentEncoder, UniCoilQueryEncoder
merge_faiss_index.py
query.py

ncoder_class_map = {
    "dpr": DprDocumentEncoder,
    "tct_colbert": TctColBertDocumentEncoder,
    "aggretriever": AggretrieverDocumentEncoder,
    "ance": AnceDocumentEncoder,
    "sentence-transformers": AutoDocumentEncoder,
    "unicoil": UniCoilDocumentEncoder,
    "auto": AutoDocumentEncoder,
}
ALLOWED_POOLING_OPTS = ["cls","mean"]