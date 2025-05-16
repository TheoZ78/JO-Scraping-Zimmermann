À placer dans le même dossier :
- html.html
- css.css
- nations.json
- athletes.json
- sports.json
- script-countries.js
- script-heatmap.js
- script-athletes.js


Comment lancer les data visualisations

1. Ouvrir le dossier dans Visual Studio Code
2. Installer l’extension « Live Server » 
3. Clic droit sur `index.html` → « Open with Live Server »


- Classement des pays par médailles (barres empilées)
- Heatmap des médailles par sport et par pays
- Top 20 des athlètes les plus médaillés


Mini Rapport : 

Étapes du processus
Scraping – Collecte des données
a) Outils et bibliothèques utilisés
- Python 
- Requests : pour récupérer les pages web 
- BeautifulSoup : pour parser le HTML 
- json : pour exporter les données nettoyées 
b) Scripts développés
- scraper_athletes.py : extraction des athlètes et de leur palmarès
 - scraper_nations.py : extraction des pays et de leurs médailles
 - scraper_sports.py : extraction des sports et répartition des médailles par pays 


Nettoyage des données
a) Problèmes rencontrés
- Données HTML « brutes » : balises, caractères spéciaux, espaces superflus
 - Incohérences de noms (ex : "USA", "United States", "United States of America")
 - Présence de doublons ou de lignes incomplètes 
b) Méthodes de nettoyage
- Suppression des balises HTML et espaces superflus :     from bs4 import BeautifulSoup     text = BeautifulSoup(raw_html, "html.parser").get_text().strip()
 - Standardisation des noms de pays, sports, athlètes (ex : passage systématique à la casse "titre", mapping des variantes)     country_map = {"USA": "United States of America", "UK": "Great Britain"}     country_clean = country_map.get(raw_country, raw_country)
 - Uniformisation des noms de médailles :     medal_clean = {"gold": "Or", "silver": "Argent", "bronze": "Bronze"}.get(raw_medal.lower(), raw_medal) 
- Suppression ou correction des enregistrements incomplets (ex : athlète sans palmarès)     if not athlete['palmares']:         continue  # On ignore cet athlète 
c) Exemple AVANT / APRÈS
Exemple brut extrait : {   "first_name": "Karina",   "last_name": "Aznavourian",   "country": "RUSSIA ",   "palmares": [     {       "medal": "gold ",       "sport": "fencing ",       "event": "Épée Team",       "date": "August 20, 2004"     }   ] }  
Après nettoyage : {   "first_name": "Karina",   "last_name": "Aznavourian",   "country": "Russia",   "palmares": [     {       "medal": "gold",       "sport": "Fencing",       "event": "Épée Team",       "date": "2004-08-20"     }   ] } 

Structuration finale et export
- Données enregistrées en JSON pour chaque entité principale :
- athletes.json
- nations.json
- sports.json
 - Respect de la structure : noms de clés homogènes, pas de doublon, tous les champs obligatoires présents
  
3. Conclusion
Grâce à ces étapes, on obtient 3 jeux de données propres, exploitables et prêts pour la visualisation et l’analyse. 
