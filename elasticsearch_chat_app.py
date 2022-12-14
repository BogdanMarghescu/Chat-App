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
    message_list = []
    resp = es.search(index=index, query={"match": {"destination": username}})
    if resp['hits']['total']['value'] > 0:
        print(f"Messages to user {username}:")
        for hit in resp['hits']['hits']:
            message_list.append({"source": hit['_source']['source'], "destination": hit['_source']['destination'], "message": hit['_source']['message'], "timestamp": hit['_source']['timestamp']})
            print(f"{hit['_source']['timestamp']} {hit['_source']['source']} --> {hit['_source']['destination']}: {hit['_source']['message']}")
    else:
        print(f"User {username} has received no messages.")
    return message_list
