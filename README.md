# RAG-BTP-Course-Skeleton

# Projet RAG Intégré pour l'Extraction et la Génération de Réponses

Ce projet vise à développer une solution complète de RAG (Retrieval Augmented Generation) en combinant plusieurs technologies afin d'extraire, traiter et exploiter des informations issues de documents PDF pour générer des réponses contextuelles à des requêtes utilisateur.

## Description du Processus

## 🛠 Installation & Setup

### 1. Create `config.ini`

```ini
[paths]
metadata = "the path to json files ( the output of the scrappers)"
pdfs = "the path to pdf files downloaded by the scrappers"
markdowns = "the path to the output dir"
data = "path where the ConceptNet RDF data will be stored"

[links]
conceptnet_assertions = https://s3.amazonaws.com/conceptnet/downloads/2019/edges/conceptnet-assertions-5.7.0.csv.gz

[qdrant_server]
qdrant_url = http://localhost:6333
dataset = conceptnet
```


1. **Extraction des Documents :**  
   Les documents sont extraits depuis le site *dispositif-rexbp* à l'aide de BeautifulSoup et Selenium.

2. **Conversion des PDF en Markdown :**  
   Un OCR nommé **PDFConverter** est utilisé pour transformer les fichiers PDF en fichiers Markdown.  
   *PDFConverter est un outil performant qui convertit efficacement le contenu des PDF en texte structuré au format Markdown.*

3. **Prétraitement des Fichiers Markdown :**  
   Les fichiers Markdown obtenus subissent un prétraitement consistant à supprimer les balises et à nettoyer le texte. Ce texte est ensuite normalisé grâce à des opérations de stemming et de lemmatisation, afin de préparer les données pour l'analyse ultérieure.

4. **Extraction des Mots-clés :**  
   Le texte prétraité est analysé par **KeyBERT** pour extraire des mots-clés pertinents pour chaque document. Ces mots-clés représentent les éléments essentiels du contenu et servent de base à la structuration des connaissances.

5. **Création du Graphe de Connaissances :**  
   Les mots-clés extraits sont utilisés pour construire un graphe de connaissances à l'aide de **Neo4j**. Ce graphe permet d'organiser et de relier les informations selon des thématiques pertinentes.

6. **Indexation Vectorielle des Chunks Markdown :**  
   Les fichiers Markdown sont découpés en segments (chunks) et transformés en vecteurs grâce à un modèle SentenceTransformer. Ces vecteurs sont ensuite stockés dans une base de données vectorielle construite avec **Qdrant**.

7. **Génération de Réponses :**  
   En combinant les informations du graphe de connaissances et de la base de données vectorielle, le système extrait les données nécessaires pour répondre aux prompts utilisateur. Ces données sont finalement transmises à **LLama3.2**, qui génère la réponse finale.

## Technologies Utilisées

- **Extraction Web :** BeautifulSoup, Selenium  
- **Conversion OCR :** PDFConverter  
- **Prétraitement de Texte :** Stemming et Lemmatisation  
- **Extraction de Mots-clés :** KeyBERT  
- **Graph Database :** Neo4j  
- **Indexation Vectorielle :** Qdrant  
- **Modèle de Génération de Réponses :** LLama3.2