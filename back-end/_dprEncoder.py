from transformers import (DPRQuestionEncoder, DPRQuestionEncoderTokenizer)

class DprQueryEncoder():

    def __init__(self, encoder_dir: str = None, tokenizer_name: str = None, device: str = 'cpu', **kwargs):
        if encoder_dir:
            self.device = device
            self.model = DPRQuestionEncoder.from_pretrained(encoder_dir)
            self.model.to(self.device)
            self.tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(tokenizer_name or encoder_dir)
            self.has_model = True
        if (not self.has_model) and (not self.has_encoded_query):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one')

    def encode(self, query: str):
        if self.has_model:
            input_ids = self.tokenizer(query, return_tensors='pt')
            input_ids.to(self.device)
            embeddings = self.model(input_ids["input_ids"]).pooler_output.detach().cpu().numpy()
            return embeddings.flatten()
        else:
            return super().encode(query)