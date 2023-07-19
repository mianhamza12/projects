import json
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from transformers import pipeline
sentences = ["python deverloper"]
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(sentences)
query_vector = embeddings[0].tolist()  # Use the first query vector

url = 'http://localhost:9200/case/_search'
headers = {'Content-Type': 'application/json'}
data = {
    "knn": {
        "field": "general_text_vector",
        "query_vector": query_vector,
        "k": 3,
        "num_candidates": 10
    },
    "_source": [
        "general_text",
        "color",
        "general_text_vector"
    ]
}

response = requests.get(url, headers=headers, json=data)
results = json.loads(response.text)
text_append = ""
for hit in results['hits']['hits']:
    doc_vector = hit['_source']['general_text_vector']
    doc_vector = [float(num) for num in doc_vector]
    doc_vector = [doc_vector]  # Convert to 2D array for cosine_similarity function
    similarity = cosine_similarity(doc_vector, [query_vector])
    print(f"Similarity: {similarity[0][0]}")
    text = hit['_source']['general_text']
    # print(f"General Text: {text}")
    text_append += text + ""

# question_answerer = pipeline("question-answering", model='lmsys/vicuna-7b-v1.3')
# context = text_append.strip()
# result = question_answerer(question="who live in karachi", context=context)
# print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")
# print("________________")
