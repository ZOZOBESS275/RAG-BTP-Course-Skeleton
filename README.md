# RAG-BTP-Course-Skeleton

# 🚀 Projet RAG Intégré pour l'Extraction et la Génération de Réponses

Ce projet propose une chaîne intelligente de traitement documentaire pour extraire, structurer et utiliser efficacement des informations à partir de fichiers PDF, dans une optique de **génération augmentée par la recherche** (*Retrieval Augmented Generation*, ou **RAG**). Il combine des technologies modernes de scraping, NLP, graphes et LLM pour offrir une expérience de question-réponse riche et contextuelle.

---

## 🔍 Vue d'ensemble du Pipeline

### 1. 🔗 Extraction des Documents
Les fichiers PDF sont récupérés depuis le site *dispositif-rexbp* grâce à une combinaison de **BeautifulSoup** (scraping statique HTML) et **Selenium** (navigation dynamique). Ce duo permet de simuler un utilisateur humain : cliquer sur les boutons, attendre le chargement de la page, et collecter automatiquement les documents ainsi que leurs métadonnées (titre, date, source, etc.).

### 2. 🔮 Conversion PDF → Markdown
Les PDF sont ensuite convertis en fichiers Markdown via **PDFConverter**, un OCR intelligent. Il interprète chaque page comme une image, extrait le texte tout en respectant la mise en forme originale (titres, tableaux, listes, etc.), puis génère un Markdown propre, lisible et structurant le contenu de façon logique. Idéal pour l'analyse sémantique ultérieure !

### 3. 📄 Nettoyage et Prétraitement des Fichiers
Les fichiers Markdown bruts sont "purifiés" via des expressions régulières (**re**). On supprime les balises HTML, les sauts de lignes multiples, les caractères parasites. Ensuite, on applique **stemming** et **lemmatisation** pour ramener les mots à leur forme de base, préparant ainsi un terrain neutre pour les prochaines étapes d'analyse.

### 4. 🔎 Extraction Intelligente de Mots-clés
C'est ici que **KeyBERT** entre en jeu. Basé sur **BERT**, ce modèle calcule des embeddings sémantiques du texte complet et de ses sous-parties, puis mesure leur similarité pour extraire les expressions-clés les plus significatives. Pas besoin d'entraînement, c'est du **zero-shot keyword extraction**, puissant et adaptatif.

### 5. 📊 Construction du Graphe de Connaissances
Les mots-clés sont transformés en nœuds et reliés par des relations pertinentes dans un graphe créé avec **Neo4j**. Ce graphe devient une représentation dynamique des concepts, permettant de naviguer dans les connaissances, de visualiser les liens entre idées, et de retrouver des informations connexes de façon fluide.

### 6. 📐 Indexation Vectorielle des Segments
Chaque document Markdown est découpé intelligemment en "chunks" via **Langchain**, pour conserver la cohérence sémantique dans chaque bloc. Ces chunks sont vectorisés à l'aide de **SentenceTransformers**, produisant des embeddings puissants. Enfin, ces vecteurs sont stockés dans **Qdrant**, une base de données vectorielle performante, prête à répondre aux requêtes par similarité.

### 7. 🧠 Génération Contextuelle de Réponses
Quand un utilisateur pose une question, celle-ci est vectorisée pour en extraire les concepts clés. Ces concepts sont utilisés pour :  
1. Interroger **Neo4j** (pour récupérer les nœuds/concepts liés),  
2. Interroger **Qdrant** (pour trouver les chunks les plus proches sémantiquement).

Les résultats combinés servent de contexte au modèle de langage **LLama3.2**, exécuté localement, qui génère alors une réponse précise, contextuelle, et enrichie par les données réelles.

---

## 🛠 Technologies Utilisées

- **Extraction Web :** BeautifulSoup, Selenium  
- **OCR / Parsing PDF :** PDFConverter  
- **Nettoyage Texte :** re, NLTK (Stemming, Lemmatisation)  
- **Mots-clés :** KeyBERT (basé sur BERT)  
- **Graphe de Connaissances :** Neo4j  
- **Vectorisation :** Langchain, SentenceTransformers  
- **Base Vectorielle :** Qdrant  
- **Modèle LLM :** LLama3.2 (exécuté localement)

---

Ce pipeline incarne une synergie moderne entre extraction, structuration et génération de connaissance. Il s'agit d'un projet modulaire, évolutif et réplicable dans plusieurs contextes industriels ou académiques. ✨
