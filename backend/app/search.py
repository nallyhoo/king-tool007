
from elasticsearch import Elasticsearch
from app.config import settings

es = Elasticsearch([settings.ELASTICSEARCH_URL])

INDEX_NAME = "videos"

def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            body={
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "description": {"type": "text"},
                        "tags": {"type": "keyword"},
                        "transcript": {"type": "text"},
                        "channel_id": {"type": "keyword"},
                        "published_at": {"type": "date"},
                        "likes": {"type": "integer"},
                        "views": {"type": "integer"},
                    }
                }
            }
        )

def index_video(video):
    es.index(index=INDEX_NAME, id=video.id, body={
        "title": video.title,
        "description": video.description,
        "tags": [tag.name for tag in video.tags],
        "transcript": video.transcript,
        "channel_id": video.channel_id,
        "published_at": video.published_at,
        "likes": video.likes,
        "views": video.views,
    })

def search_videos(query: str):
    response = es.search(
        index=INDEX_NAME,
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "description", "transcript", "tags"],
                    "fuzziness": "AUTO",
                }
            }
        }
    )
    return [hit["_source"] for hit in response["hits"]["hits"]]
