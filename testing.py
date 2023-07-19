from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

# query to get minimum results range more than 10

# query = {
#   "query": {
#     "range": {
#       "minimum_range": {
#         "gt": 10
#       }
#     }
#   }
# }

# query to get results against MernStack

query = {
  "query": {
    "fuzzy": {
      "title": {
        "value": "MernStack"
      }
    }
  }
}


response = es.search(index="accept", body=query)

# Process the results
for hit in response['hits']['hits']:
    source = hit['_source']
    title = source['title']
    summary = source['summary_text']
    min = source['minimum_range']



    print(f"Title: {title}")
    print(f"Summary: {summary}")
    print(f"Minimum_range: {min}")
    print("---")
