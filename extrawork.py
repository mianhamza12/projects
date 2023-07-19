from elasticsearch import Elasticsearch
from transformers import pipeline

# Elasticsearch connection settings
es_host = "localhost"
es_port = 9200
es_index = "neural_index1"

# Zero-shot Q&A model settings
model_name = "valhalla/t5-base-qa-qg-hl"
candidate_answers = ["python developer"]
es = Elasticsearch([{'host': es_host, 'port': es_port}])
es_query = {
    "query": {
        "match": {
            "your_field_name": "your_search_term"
        }
    },
    "size": 10
}

response = es.search(index=es_index, body=es_query)

# Initialize the zero-shot Q&A pipeline
qa_pipeline = pipeline("question-answering", model=model_name)

# Process each document and perform zero-shot Q&A
for hit in response["hits"]["hits"]:
    document = hit["_source"]["general_text"]

    # Ask a question and get the answer
    question = "python developer"
    result = qa_pipeline(question, document, candidate_answers)

    # Extract the relevant information from the result
    answer = result["answer"]
    confidence = result["score"]

    # Display the question, answer, and confidence score
    print("Question:", question)
    print("Answer:", answer)
    print("Confidence Score:", confidence)
    print("-----------------------------")

