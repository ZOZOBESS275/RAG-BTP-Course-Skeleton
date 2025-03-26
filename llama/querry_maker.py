from neo4j_engine.neo4j_comunication import get_querry_related_keywords # type: ignore
from Qdrant.qdrant_comunication import retrieve_relevant_chunks # type: ignore
def expand_query(user_query, top_k=5):
    # 1) Expand user query with Neo4j
    expansions = get_querry_related_keywords(user_query)
    # 2) Retrieve relevant chunks from Qdrant
    docs = retrieve_relevant_chunks(user_query, expansions, top_k=top_k)
    context_text = ""
    for doc in docs:
        payload = doc[1][0].payload
        context_text += f"Fichier: {payload['file']}\nChunk: {payload['chunk']}\n\n"
    full_prompt = f"""
    CONTEXTE:
    {context_text}

    QUESTION UTILISATEUR:
    {user_query}

    RÉPONSE ATTENDUE (en utilisant uniquement les informations ci-dessus) :
    """
    return full_prompt