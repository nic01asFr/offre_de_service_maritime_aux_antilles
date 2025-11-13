#!/usr/bin/env python3
"""
Analyse la qualité des tracés de routes maritimes dans export.geojson
- Identifie les lignes droites vs tracés détaillés
- Calcule des métriques de qualité
- Génère un rapport avec recommandations
"""

import json
import math
from typing import Dict, List, Tuple

def haversine_distance(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """Calcule la distance en km entre deux points GPS"""
    R = 6371  # Rayon de la Terre en km

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c

def analyze_route_geometry(coordinates: List[List[float]]) -> Dict:
    """Analyse la géométrie d'une route"""
    num_points = len(coordinates)

    # Calculer la distance totale du tracé
    total_distance = 0
    for i in range(len(coordinates) - 1):
        lon1, lat1 = coordinates[i]
        lon2, lat2 = coordinates[i + 1]
        total_distance += haversine_distance(lon1, lat1, lon2, lat2)

    # Calculer la distance directe (vol d'oiseau)
    if num_points >= 2:
        start_lon, start_lat = coordinates[0]
        end_lon, end_lat = coordinates[-1]
        direct_distance = haversine_distance(start_lon, start_lat, end_lon, end_lat)
    else:
        direct_distance = 0

    # Ratio de sinuosité (1.0 = ligne droite parfaite)
    sinuosity = total_distance / direct_distance if direct_distance > 0 else 1.0

    # Déterminer le type de tracé
    if num_points == 2:
        trace_type = "LIGNE_DROITE"
        quality_score = 1  # Faible qualité
    elif num_points <= 5:
        trace_type = "TRACE_SIMPLE"
        quality_score = 2
    elif num_points <= 10:
        trace_type = "TRACE_MOYEN"
        quality_score = 3
    else:
        trace_type = "TRACE_DETAILLE"
        quality_score = 4  # Haute qualité

    return {
        'num_points': num_points,
        'total_distance_km': round(total_distance, 2),
        'direct_distance_km': round(direct_distance, 2),
        'sinuosity': round(sinuosity, 3),
        'trace_type': trace_type,
        'quality_score': quality_score
    }

def main():
    print("Analyse de la qualite des traces maritimes...")
    print("=" * 60)

    # Charger le GeoJSON
    with open('export.geojson', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Total features dans le GeoJSON: {len(data['features'])}")

    # Analyser chaque route
    routes_analysis = []
    stats = {
        'LIGNE_DROITE': 0,
        'TRACE_SIMPLE': 0,
        'TRACE_MOYEN': 0,
        'TRACE_DETAILLE': 0,
        'abandoned': 0,
        'total_ferry_routes': 0
    }

    for feature in data['features']:
        props = feature['properties']
        geom = feature['geometry']

        # Ignorer les routes non-ferry ou abandonnées
        if props.get('route') != 'ferry':
            continue

        stats['total_ferry_routes'] += 1

        if props.get('abandoned') or props.get('disused'):
            stats['abandoned'] += 1
            continue

        if geom['type'] != 'LineString':
            continue

        # Analyser la géométrie
        analysis = analyze_route_geometry(geom['coordinates'])

        # Ajouter les métadonnées
        route_info = {
            'name': props.get('name', 'Sans nom'),
            'operator': props.get('operator', 'Non spécifié'),
            'osm_id': props.get('@id', 'N/A'),
            **analysis
        }

        routes_analysis.append(route_info)
        stats[analysis['trace_type']] += 1

    # Trier par score de qualité (du pire au meilleur)
    routes_analysis.sort(key=lambda x: x['quality_score'])

    # Générer le rapport
    print("\n*** STATISTIQUES GLOBALES ***")
    print("-" * 60)
    print(f"Total routes ferry: {stats['total_ferry_routes']}")
    print(f"Routes abandonnees: {stats['abandoned']}")
    print(f"Routes actives analysees: {len(routes_analysis)}")
    print()
    print("Repartition par qualite de trace:")
    print(f"  [ROUGE] Lignes droites (2 points): {stats['LIGNE_DROITE']} ({stats['LIGNE_DROITE']/len(routes_analysis)*100:.1f}%)")
    print(f"  [ORANGE] Traces simples (3-5 pts): {stats['TRACE_SIMPLE']} ({stats['TRACE_SIMPLE']/len(routes_analysis)*100:.1f}%)")
    print(f"  [JAUNE] Traces moyens (6-10 pts): {stats['TRACE_MOYEN']} ({stats['TRACE_MOYEN']/len(routes_analysis)*100:.1f}%)")
    print(f"  [VERT] Traces detailles (>10 pts): {stats['TRACE_DETAILLE']} ({stats['TRACE_DETAILLE']/len(routes_analysis)*100:.1f}%)")

    # Routes nécessitant amélioration (lignes droites)
    print("\n[ROUGE] ROUTES NECESSITANT AMELIORATION (Lignes droites)")
    print("-" * 60)

    straight_routes = [r for r in routes_analysis if r['trace_type'] == 'LIGNE_DROITE']
    for i, route in enumerate(straight_routes[:15], 1):  # Top 15
        print(f"\n{i}. {route['name']}")
        print(f"   Operateur: {route['operator']}")
        print(f"   Distance: {route['direct_distance_km']} km")
        print(f"   OSM ID: {route['osm_id']}")
        print(f"   [!] Trace simplifie en ligne droite - necessite waypoints intermediaires")

    # Routes bien tracées
    print("\n\n[VERT] ROUTES BIEN TRACEES (Exemples)")
    print("-" * 60)

    detailed_routes = [r for r in routes_analysis if r['trace_type'] == 'TRACE_DETAILLE']
    for i, route in enumerate(detailed_routes[:5], 1):  # Top 5
        print(f"\n{i}. {route['name']}")
        print(f"   Operateur: {route['operator']}")
        print(f"   Points de trace: {route['num_points']}")
        print(f"   Distance trace: {route['total_distance_km']} km")
        print(f"   Distance directe: {route['direct_distance_km']} km")
        print(f"   Sinuosite: {route['sinuosity']} (1.0 = ligne droite)")
        print(f"   [OK] Trace detaille et realiste")

    # Sauvegarder le rapport détaillé en JSON
    report = {
        'timestamp': '2025-01-13',
        'statistics': stats,
        'total_analyzed': len(routes_analysis),
        'routes': routes_analysis
    }

    with open('route_quality_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n\n[SAVE] Rapport detaille sauvegarde dans: route_quality_report.json")

    # Recommandations
    print("\n\n*** RECOMMANDATIONS ***")
    print("-" * 60)
    print(f"1. {stats['LIGNE_DROITE']} routes sont des lignes droites simples")
    print("   -> Necessitent l'ajout de waypoints intermediaires realistes")
    print()
    print("2. Pour ameliorer les traces:")
    print("   - Utiliser des outils comme JOSM (Java OpenStreetMap Editor)")
    print("   - Suivre les routes maritimes reelles visibles sur satellite")
    print("   - Ajouter des waypoints aux points de changement de direction")
    print("   - Respecter les chenaux de navigation et zones de passage")
    print()
    print("3. Sources pour traces precis:")
    print("   - Images satellite haute resolution")
    print("   - Donnees AIS (Automatic Identification System) des navires")
    print("   - Cartes marines officielles du SHOM")
    print("   - Traces GPS de trajets reels")

    print("\n" + "=" * 60)
    print("[OK] Analyse terminee !")

if __name__ == '__main__':
    main()
