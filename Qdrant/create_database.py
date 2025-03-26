import pandas as pd
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

server = config["Qdrant"]["server"]
batch_size = config["Qdrant"]["creation_batch_size"]

df = pd.read_csv("CHUNKS\\file_chunks.csv") 
model = SentenceTransformer("dangvantuan/sentence-camembert-base")

# Let's quickly check the embedding dimension:
dummy_vector = model.encode("texte de test")
dim = len(dummy_vector)  # This will be used in Qdrant's vector params
print(f"Embedding dimension: {dim}")



# Adjust host/port if Qdrant is elsewhere:
client = QdrantClient(url=server)  # or QdrantClient("localhost", port=6333)

# Create or recreate a collection
collection_name = "PROJET_RCRA2"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
)

# Now, embed and upsert each CSV chunk as a separate point in Qdrant
points_to_upsert = []
for idx, row in tqdm(df.iterrows()):
    text_chunk = row["chunk"]
    file_id = row["file"]  # might be useful metadata
    vector = model.encode(text_chunk)

    # Create a unique ID for each chunk row
    point_id = idx  
    payload = {
        "file": file_id, 
        "chunk": text_chunk
    }

    # Construct a PointStruct
    points_to_upsert.append(
        PointStruct(
            id=point_id,
            vector=vector.tolist(),
            payload=payload
        )
    )
    


for i in range(0, len(points_to_upsert), batch_size):
    batch = points_to_upsert[i:i + batch_size]
    client.upsert(
        collection_name=collection_name,
        points=batch
    )
    print(f"✅ Uploaded batch {i} to {i + len(batch)} from {len(points_to_upsert)}")