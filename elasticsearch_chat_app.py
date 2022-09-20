from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch('http://127.0.0.1:9200')


def send_message(es, username_src, username_dest, message, index="messages"):
    doc = {
        'source': username_src,
        "destination": username_dest,
        "message": message,
        'timestamp': datetime.now(),
    }
    resp = es.index(index=index, document=doc)
    es.indices.refresh(index=index)
    if resp['result'] == 'created':
        print(f'Message from {username_src} to {username_dest} was sent succesfully.')
    else:
        print(f'Message from {username_src} to {username_dest} was NOT sent.')


def get_messages(es, username, index="messages"):
    resp = es.search(index=index, query={"match": {"source": username}})
    if resp['hits']['total']['value'] > 0:
        print(f"Messages from user {username}:")
        for hit in resp['hits']['hits']:
            print(f"{hit['_source']['timestamp']} {hit['_source']['source']} --> {hit['_source']['destination']}: {hit['_source']['message']}")
    else:
        print(f"User {username} has no messages sent.")
