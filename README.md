# 🗺️ Cartographie Services Maritimes Antilles

Cartographie interactive des services maritimes dans les Antilles françaises (Guadeloupe, Martinique, Saint-Martin) avec intégration des données OpenStreetMap.

## 🚢 Fonctionnalités

- **Visualisation interactive** des routes maritimes avec Leaflet.js
- **Données OpenStreetMap** : Routes de ferry issues d'export.geojson
- **Analyse thématique** : Liaisons locales, régionales, internationales, navettes urbaines
- **Informations détaillées** : Compagnies, horaires, tarifs, fréquences
- **Filtres dynamiques** par territoire et compagnie
- **Recherche** de ports, îles et compagnies
- **Export CSV** des données

## 📂 Fichiers principaux

- **cartographie_maritime_antilles_v11_analytics.html** : Carte interactive principale
- **export.geojson** : Données des routes maritimes OpenStreetMap
- Documentation et analyses dans les fichiers Markdown

## 🌐 Accès en ligne

Cette carte est hébergée sur GitHub Pages : [Accéder à la carte](https://votre-username.github.io/cartographie-services-maritimes-antilles/)

## 🚀 Utilisation locale

Pour utiliser la carte localement avec les données GeoJSON, lancez un serveur web :

```bash
python -m http.server 8000
```

Puis ouvrez : http://localhost:8000/cartographie_maritime_antilles_v11_analytics.html

## 📊 Sources de données

- **OpenStreetMap** : Routes maritimes (export.geojson)
- **Recherche documentaire** : Sites des compagnies maritimes, horaires officiels
- **Données 2025** : Compilation exhaustive des liaisons maritimes

## 🏝️ Zones couvertes

- **Guadeloupe** : Les Saintes, Marie-Galante, La Désirade
- **Martinique** : Fort-de-France, navettes baie des Trois-Îlets
- **Saint-Martin/Sint Maarten** : Liaisons vers Saint-Barthélemy, Anguilla, Saba

## 📝 Licence

Données OpenStreetMap sous licence ODbL
Carte développée pour l'analyse du transport maritime aux Antilles

## 👤 Auteur

Nicolas Laval - Analyse et cartographie des services maritimes
