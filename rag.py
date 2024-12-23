import openai
from transformers import AutoTokenizer, AutoModel
import faiss
import numpy as np
import torch
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


openai.api_key = config['openai']['api_key']

class SimpleRetriever:
    def __init__(self, document_texts):
        self.document_texts = document_texts
        self.index = faiss.IndexFlatL2(768)  
        self.embeddings = self.embed_texts(self.document_texts)
        self.index.add(self.embeddings)
    
    def embed_texts(self, texts):
        tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')


        encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = model(**encoded_input)
        embeddings = model_output.last_hidden_state.mean(dim=1) 
        return embeddings.cpu().numpy()

    def retrieve(self, query, top_k=5):
        query_embedding = self.embed_texts([query])
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.document_texts[i] for i in indices[0]]


def generate_response_with_context(query, retriever, top_k=5):

    retrieved_docs = retriever.retrieve(query, top_k)

    context = "\n\n".join(retrieved_docs)
    prompt = f"Context: {context}\n\nQuery: {query}\n\nAnswer:"

    response = openai.Completion.create(
        engine="gpt-4o", 
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7
    )

    return response['choices'][0]['text'].strip()

document_corpus = [
    "Document 1 content about AI.",
    "Document 2 content about machine learning.",
    "Document 3 content about deep learning."
]

retriever = SimpleRetriever(document_corpus)
query = "What is the relationship between AI and deep learning?"
response = generate_response_with_context(query, retriever)
print(response)