from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import configparser
from sentence_transformers import SentenceTransformer



def retrieve_relevant_chunks(user_query, keywords , top_k=5):
    """
    - Combine the user query with keywords
    - Embed once
    - Query Qdrant for the top_k most similar chunks
    """
    sentence_transformer = SentenceTransformer("dangvantuan/sentence-camembert-base")
    config = configparser.ConfigParser()
    config.read("config.ini")

    server = config["Qdrant"]["server"]
    collection_name = config["Qdrant"]["collection_name"]
    # Adjust host/port if Qdrant is elsewhere:
    client = QdrantClient(url=server)  # or QdrantClient("localhost", port=6333)


    if keywords:
        expansion_text = " ".join(keywords)
        augmented_text = user_query + " " + expansion_text
    else:
        augmented_text = user_query
    
    query_vector = sentence_transformer.encode(augmented_text)

    # Qdrant query
    results = client.query_points(
        collection_name=collection_name,
        query=query_vector.tolist(),
        limit=top_k
    )
    
    # 'results' will be a list of ScoredPoint objects
    # Each contains 'payload' (with our stored chunk)
    return results
