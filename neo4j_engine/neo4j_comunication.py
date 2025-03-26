from neo4j import GraphDatabase

import configparser



def get_related_keywords(keyword):
    config = configparser.ConfigParser()

    # Read the ini file
    config.read("config.ini")

    # Access values
    server = config["neo4j"]["server"]
    user = config["neo4j"]["user"]
    password = config["neo4j"]["password"]


    driver = GraphDatabase.driver(server, auth=(user, password))
    
    query = """
    MATCH (n)
    WHERE toLower(n.name) CONTAINS toLower($keyword)
    MATCH (n)--(related)
    RETURN DISTINCT related.name AS keyword, labels(related) AS type
    """
    with driver.session() as session:
        result = session.run(query, keyword=keyword)
        return [record["keyword"] for record in result]

def get_querry_related_keywords(user_query):
    """
    Naive approach: split user query into tokens 
    and gather related keywords from Neo4j.
    """
    tokens = user_query.lower().split()
    print(tokens)
    all_expanded = set()
    for token in tokens:
        expansions = get_related_keywords(token)
        all_expanded.update(expansions)
    return list(all_expanded)