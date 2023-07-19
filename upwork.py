import feedparser
from bs4 import BeautifulSoup
import re
from elasticsearch import Elasticsearch
import schedule
import time
import json
import json
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

es = Elasticsearch(["http://localhost:9200"])
index_name = "accept"
# index_settings = {
#     "settings": {
#         "number_of_shards": 1,
#         "number_of_replicas": 0
#     },
#     "mappings": {
#         "properties": {
#             "title": {"type": "text"},
#             "summary_text": {"type": "text"},
#             "country": {"type": "keyword"},
#             "skills_list": {"type": "keyword"},
#             "category": {"type": "keyword"},
#             "minimum_range": {"type": "float"},
#             "maximum_range": {"type": "float"},
#             "job_link": {"type": "text"},
#             "pub_date": {"type": "date", "format": "EEE, dd MMM yyyy HH:mm:ss Z"},
#             "query_vector": {"type": "float"},
#             "priority": {"type": "float"},
#             "case_study": {"type": "text"},
#             "text_vector": {"type": "float"}
#         }
#     }
# }


reject_index = "reject"
# index_settings = {
#     "settings": {
#         "number_of_shards": 1,
#         "number_of_replicas": 0
#     },
#     "mappings": {
#         "properties": {
#             "title": {"type": "text"},
#             "summary_text": {"type": "text"},
#             "country": {"type": "keyword"},
#             "skills_list": {"type": "keyword"},
#             "category": {"type": "keyword"},
#             "minimum_range": {"type": "float"},
#             "maximum_range": {"type": "float"},
#             "job_link": {"type": "text"},
#             "pub_date": {"type": "date", "format": "EEE, dd MMM yyyy HH:mm:ss Z"},
#             "query_vector": {"type": "flot"},
#             "priority": {"type": "float"},
#             "case_study": {"type": "text"},
#             "text-vector": {"type": "float"}
#         }
#     }
# }
#
INDEX_NAME = "case"
output_file = "/home/spyresync/Desktop/project/upwork.txt"


def parse_and_save_data():
    url = "https://www.upwork.com/ab/feed/jobs/rss?q=django&sort=recency&category2_uid=531770282580668421%2C531770282580668419%2C531770282580668418&paging=0%3B10&api_params=1&securityToken=744c05986f0656e00113dec6d4943ad992559d63b66ea25536c09a8861070e7ce51b72acd4e7034d45557e0eeb06d871f287562b9bc3023e97e6005a674b4b9c&userUid=1531232597027590144&orgUid=1531232597027590145"
    feed = feedparser.parse(url)
    for entry in feed.entries:
        title = entry.title
        summary_text = BeautifulSoup(entry.summary, "html.parser").get_text()
        match = re.search(r'Country: (.+)', summary_text)
        if match:
            country = match.group(1)
        match = re.search(r'Skills:(.+)', summary_text)
        if match:
            skills = match.group(1).strip()
            skills_list = [skill.strip() for skill in skills.split(',')]
        match = re.search(r'Category:(.+?)Skills', summary_text)
        if match:
            category = match.group(1).strip()
        match = re.search(r'Hourly Range: \$([\d\.]+)-\$([\d\.]+)', summary_text)
        if match:
            minimum_range = match.group(1).strip()
            maximum_range = match.group(2).strip()
        else:
            maximum_range = None
            minimum_range = None

        job_link = "Job Link:", entry.link
        pub_date = "Job Published Date:", entry.published
        print("------------")

        sentences = [title, summary_text, country, skills_list, category, maximum_range, minimum_range, job_link,
                     pub_date]
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        embeddings = model.encode(sentences)
        query_vector = embeddings[0].tolist()  # Use the first quer  y vector

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
        similarity_list = []
        general_list = []
        text_append = ""
        for hit in results['hits']['hits']:
            doc_vector = hit['_source']['general_text_vector']
            doc_vector = [float(num) for num in doc_vector]
            doc_vector = [doc_vector]  # Convert to 2D array for cosine_similarity function
            similarity = cosine_similarity(doc_vector, [query_vector])
            round_sim = round(similarity[0][0], 2)
            text = hit['_source']['general_text']
            text_vector = model.encode(text)
            # print(text)
            document = {
                "title": title,
                "summary_text": summary_text,
                "country": country,
                "skills_list": skills_list,
                "category": category,
                "maximum_range": float(maximum_range) if maximum_range else None,
                "minimum_range": float(minimum_range) if maximum_range else None,
                "job_link": job_link,
                "pub_date": pub_date,
                "query_text": query_vector,
                "priority": similarity_list,
                "case_study": general_list,
                "text_vector": text_vector
            }
            if round_sim >= 0.30:
                similarity_list.append(round_sim)
                text = hit['_source']['general_text']
                general_list.append(text)
                es.index(index=index_name, body=document)
            else:
                similarity_list.append(round_sim)
                text = hit['_source']['general_text']
                general_list.append(text)
                es.index(index=reject_index, body=document)


parse_and_save_data()
print("done")
