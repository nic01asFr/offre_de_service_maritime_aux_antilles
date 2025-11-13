# Routes maritimes à corriger - Segments en ligne droite

## Analyse effectuée le 2025-01-13

Sur **123 routes maritimes** actives analysées, **55 routes** présentent des segments longs (>5km) qui créent des lignes droites non réalistes.

---

## 🔴 Routes PRIORITAIRES Antilles françaises

### 1. Ligne Pointe-à-Pitre → Marie-Galante
- **OSM ID** : way/330784023
- **Distance totale** : 48.01 km
- **Segments à améliorer** : 4
- **Plus long segment** : 9.22 km (ligne droite)
- **Détails** :
  - Segment 13 : 8.32 km
  - Segment 15 : 9.22 km ⚠️
  - Segment 16 : 6.92 km

**Action** : Ajouter 5-8 waypoints intermédiaires sur le segment de 9.22 km pour suivre le chenal maritime réel.

---

### 2. Ligne Pointe-à-Pitre → Les Saintes
- **OSM ID** : way/126546461
- **Distance totale** : 45.85 km
- **Segments à améliorer** : 2
- **Plus long segment** : 10.26 km (ligne droite)
- **Détails** :
  - Segment 8 : **10.26 km** ⚠️⚠️ (le plus problématique)
  - Segment 9 : 5.31 km

**Action** :
1. Diviser le segment de 10.26 km en 3-4 segments avec waypoints intermédiaires
2. Suivre la route maritime passant au large de la Basse-Terre
3. Utiliser images satellite ou données AIS pour tracé réaliste

---

### 3. Fort-de-France → Castries (Sainte-Lucie)
- **OSM ID** : way/1120991882
- **Distance totale** : 69.96 km
- **Segments à améliorer** : 4
- **Plus long segment** : 18.39 km (ligne droite)
- **Détails** :
  - Segment 14 : 12.82 km
  - Segment 15 : 11.03 km
  - Segment 16 : **18.39 km** ⚠️⚠️

**Action** : Route internationale majeure - priorité haute. Ajouter 6-10 waypoints pour suivre le passage entre la Martinique et Sainte-Lucie.

---

## 📋 Méthodologie de correction

### Outils recommandés

1. **JOSM (Java OpenStreetMap Editor)**
   - Télécharger : https://josm.openstreetmap.de/
   - Permet édition avancée des routes maritimes
   - Support images satellite superposées

2. **Sources de données pour tracés réalistes**
   - **Marine Traffic** : https://www.marinetraffic.com/
     - Données AIS temps réel des navires
     - Affiche les trajectoires réelles
   - **Google Earth** : Images satellite haute résolution
   - **Cartes SHOM** : Cartes marines officielles françaises
   - **Bing Maps** : Images satellite alternatives

### Processus étape par étape

#### 1. Préparation
```bash
# Installer JOSM
# Configurer compte OpenStreetMap
# Activer couche images satellite dans JOSM
```

#### 2. Édition d'une route

1. **Ouvrir la route dans JOSM**
   - Rechercher par OSM ID (ex: way/126546461)
   - Télécharger la zone

2. **Activer l'imagerie satellite**
   - Menu Imagery → Bing aerial imagery (ou Esri World Imagery)
   - Superposer la route actuelle

3. **Identifier le passage maritime réel**
   - Observer les images satellite
   - Vérifier sur Marine Traffic les trajectoires AIS
   - Repérer les chenaux de navigation

4. **Ajouter des waypoints**
   - Clic droit sur le segment → Add node
   - Placer 1 waypoint tous les 2-3 km
   - Suivre la courbure naturelle de la route
   - Respecter les passages entre îles/obstacles

5. **Vérifier et valider**
   - Vérifier que la route ne traverse pas de terre
   - S'assurer de la cohérence avec routes adjacentes
   - Upload vers OpenStreetMap

#### 3. Exemple concret : Pointe-à-Pitre → Les Saintes

Segment problématique actuel :
```
Point A : [-61.529935, 16.211890]
Point B : [-61.509936, 16.121636]
Distance : 10.26 km en ligne droite ❌
```

Correction proposée (ajouter waypoints) :
```
Point A : [-61.529935, 16.211890]  (départ Pointe-à-Pitre)
WP1     : [-61.527000, 16.195000]  (sortie baie)
WP2     : [-61.522000, 16.175000]  (au large Gosier)
WP3     : [-61.517000, 16.150000]  (passage)
WP4     : [-61.513000, 16.135000]  (approche)
Point B : [-61.509936, 16.121636]  (arrivée)
```

---

## 📊 Statistiques complètes

- **Total routes analysées** : 123
- **Routes avec segments longs** : 55 (45%)
- **Routes parfaitement tracées** : 68 (55%)

### Répartition par zone

| Zone | Routes OK | Routes à améliorer |
|------|-----------|-------------------|
| Guadeloupe | 12 | 8 |
| Martinique | 5 | 3 |
| Saint-Martin | 3 | 2 |
| Îles anglophones | 48 | 42 |

---

## 🎯 Plan d'action

### Phase 1 : Routes Antilles françaises (Priorité HAUTE)
- [ ] Pointe-à-Pitre → Les Saintes (way/126546461)
- [ ] Pointe-à-Pitre → Marie-Galante (way/330784023)
- [ ] Fort-de-France → Castries (way/1120991882)

### Phase 2 : Routes régionales (Priorité MOYENNE)
- [ ] Kingstown → Union Island
- [ ] Antigua → Montserrat

### Phase 3 : Routes longue distance (Priorité BASSE)
- [ ] Trinidad → Tobago
- [ ] Charlotte Amalie → Virgin Gorda

---

## 📚 Ressources

### Documentation OpenStreetMap
- Tag:route=ferry : https://wiki.openstreetmap.org/wiki/Tag:route%3Dferry
- Marine navigation : https://wiki.openstreetmap.org/wiki/Marine_navigation

### Outils d'analyse
- **straight_segments_report.json** : Rapport complet avec tous les segments
- **identify_straight_segments.py** : Script d'analyse (seuil configurable)

### Contact
Pour contribuer aux corrections sur OpenStreetMap ou signaler d'autres problèmes, créer une issue sur le repo GitHub.

---

**Dernière mise à jour** : 2025-01-13
**Analysé par** : Claude Code + analyze_route_quality.py + identify_straight_segments.py
