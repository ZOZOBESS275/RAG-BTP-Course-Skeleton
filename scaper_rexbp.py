import os
import json
import requests
from bs4 import BeautifulSoup
import time
import re  # Pour nettoyer les noms de fichiers

# URL de base pour la pagination
base_url = "https://www.dispositif-rexbp.com/ressources"

# Dossiers pour sauvegarder les fichiers JSON et PDF
json_folder = "output_json"
pdf_folder = "pdf_files"
os.makedirs(json_folder, exist_ok=True)
os.makedirs(pdf_folder, exist_ok=True)

# Ignorer certaines images inutiles
ignored_images = [
    "https://www.dispositif-rexbp.com/sites/default/files/logo-rex-couleurs.png"
]

# Fonction pour nettoyer les noms de fichiers
def sanitize_filename(filename):
    # Remplace les caractères non autorisés par un underscore
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

# Fonction pour télécharger un fichier
def download_file(url, folder, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(folder, filename)
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Fichier téléchargé : {file_path}")
        else:
            print(f"Erreur de téléchargement pour {url} (Code: {response.status_code})")
    except Exception as e:
        print(f"Erreur lors du téléchargement de {url} : {e}")

# Fonction pour extraire les données d'une page HTML
def extract_data_from_html(page_url):
    # Envoyer une requête GET pour obtenir le contenu de la page
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Erreur lors de l'accès à {page_url} (Code: {response.status_code})")
        return None

    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraire les données spécifiques
    data = {}
    title_span = soup.find("h1").find("span") if soup.find("h1") else None
    data["Titre"] = title_span.get_text(strip=True) if title_span else "Titre inconnu"

    content_block = soup.find("div", {"id": "block-rexbp-content"})
    if content_block:
        # Texte principal
        full_text = content_block.find("div", class_="full-texte")
        data["Texte"] = full_text.get_text(strip=True) if full_text else "Texte non disponible"

        # Images
        data["Images"] = []
        image_tag = content_block.find("img", src=True)
        if image_tag:
            img_url = image_tag["src"]
            if img_url not in ignored_images:
                full_url = requests.compat.urljoin(base_url, img_url)
                data["Images"].append(full_url)
                
        # Videos
        data["Videos"] = []        
        video_tag = content_block.find('div', class_='video-miniature')
        data["Videos"].append(video_tag['data-url'] if video_tag else None)
        
        # PDF
        data["PDFs"] = []
        pdf_link = content_block.find("a", class_="file-download", href=True)
        if pdf_link:
            pdf_url = pdf_link["href"]
            full_url = requests.compat.urljoin(base_url, pdf_url)
            data["PDFs"].append(full_url)

            # Télécharger le PDF
            pdf_filename = sanitize_filename(f"{data['Titre']}.pdf")
            #download_file(full_url, pdf_folder, pdf_filename)

        
        
        data["Thématique"] = []
        field_thematique = content_block.find('div', class_='field_thematique')
        if field_thematique:
            # Search for all nested elements with class="name" within the parent
            name_divs = field_thematique.find_all('div', class_='name')
            if name_divs:
                for name_div in name_divs:
                    data["Thématique"].append(name_div.get_text(strip=True))  # Extract and clean the text
            else:
                print("Non disponible")
        else:
            print("Non disponible")

        

       
        data["Type_document"] = []
        filed_type_document = content_block.find('div', class_='field_type_document')
        if filed_type_document:
            # Search for the nested element with class="name" within the parent
            name_div = filed_type_document.find('div', class_='name')
            if name_div:
                data["Type_document"].append(name_div.get_text(strip=True)) # Extract and clean the text  
            else:
                print("Non disponible")
        else:
            print("Non disponible")


        # Lien de la page
        data["Lien"] = page_url
    
    else:
        data["Texte"] = "Texte non disponible"
        data["Images"] = []
        data["PDFs"] = []
        data["Thématique"] = "Non disponible"
        data["Catégorie"] = "Non disponible"
        data["Lien"] = page_url
        data["Videos"] = "Non disponible"

    return data

# Fonction pour scraper toutes les pages et suivre la pagination
def scrape_all_pages(base_url):
    current_page_url = base_url
    while current_page_url:
        print(f"Scraping page : {current_page_url}")
        response = requests.get(current_page_url)
        if response.status_code != 200:
            print(f"Erreur lors de l'accès à la page {current_page_url} (Code: {response.status_code})")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Récupérer les liens des ressources
        resource_links = [requests.compat.urljoin(base_url, a["href"]) for a in soup.find_all("a", href=True) if "/ressource/" in a["href"]]

        # Traiter chaque ressource
        for resource_url in resource_links:
            resource_data = extract_data_from_html(resource_url)
            if resource_data:
                # Nettoyer le titre pour en faire un nom de fichier valide
                json_filename = f"{sanitize_filename(resource_data['Titre'])}.json"
                json_path = os.path.join(json_folder, json_filename)

                # Sauvegarder les données au format JSON
                with open(json_path, "w", encoding="utf-8") as json_file:
                    json.dump(resource_data, json_file, indent=4, ensure_ascii=False)
                print(f"JSON sauvegardé : {json_path}")

        # Vérifier le lien pour la page suivante
        next_page = soup.find("a", rel="next")
        if next_page and "href" in next_page.attrs:
            current_page_url = requests.compat.urljoin(base_url, next_page["href"])
            time.sleep(1)  # Pause pour éviter de surcharger le serveur
        else:
            print("Toutes les pages ont été récupérées.")
            break

# Lancer le scraping
scrape_all_pages(base_url)
print("Scraping terminé avec succès.")


