#!/usr/bin/env python3
"""
Identifie les segments en ligne droite dans les routes maritimes
Détecte les grands sauts entre waypoints qui devraient avoir des points intermédiaires
"""

import json
import math
from typing import List, Tuple, Dict

def haversine_distance(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """Calcule la distance en km entre deux points GPS"""
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def analyze_route_segments(coordinates: List[List[float]], threshold_km: float = 5.0) -> Dict:
    """Analyse les segments d'une route et identifie les segments trop longs"""
    long_segments = []
    total_distance = 0

    for i in range(len(coordinates) - 1):
        lon1, lat1 = coordinates[i]
        lon2, lat2 = coordinates[i + 1]
        distance = haversine_distance(lon1, lat1, lon2, lat2)
        total_distance += distance

        if distance > threshold_km:
            long_segments.append({
                'segment_index': i,
                'from': [lon1, lat1],
                'to': [lon2, lat2],
                'distance_km': round(distance, 2)
            })

    return {
        'total_points': len(coordinates),
        'total_distance_km': round(total_distance, 2),
        'long_segments': long_segments,
        'num_long_segments': len(long_segments),
        'needs_improvement': len(long_segments) > 0
    }

def main():
    print("Identification des segments en ligne droite...")
    print("=" * 60)

    with open('export.geojson', 'r', encoding='utf-8') as f:
        data = json.load(f)

    problematic_routes = []

    for feature in data['features']:
        props = feature['properties']
        geom = feature['geometry']

        # Filtrer routes ferry actives
        if props.get('route') != 'ferry':
            continue
        if props.get('abandoned') or props.get('disused'):
            continue
        if geom['type'] != 'LineString':
            continue

        name = props.get('name', 'Sans nom')
        analysis = analyze_route_segments(geom['coordinates'], threshold_km=5.0)

        if analysis['needs_improvement']:
            route_info = {
                'name': name,
                'osm_id': props.get('@id', 'N/A'),
                'operator': props.get('operator', 'Non specifie'),
                **analysis
            }
            problematic_routes.append(route_info)

    # Trier par nombre de segments longs
    problematic_routes.sort(key=lambda x: x['num_long_segments'], reverse=True)

    print(f"\nTotal routes analysees: {len([f for f in data['features'] if f['properties'].get('route') == 'ferry'])}")
    print(f"Routes avec segments longs (>5km): {len(problematic_routes)}")
    print()

    print("ROUTES NECESSITANT AMELIORATION")
    print("-" * 60)

    for i, route in enumerate(problematic_routes[:15], 1):
        print(f"\n{i}. {route['name']}")
        print(f"   OSM ID: {route['osm_id']}")
        print(f"   Points totaux: {route['total_points']}")
        print(f"   Distance totale: {route['total_distance_km']} km")
        print(f"   Segments longs: {route['num_long_segments']}")

        for seg in route['long_segments'][:3]:  # Afficher max 3 segments
            print(f"     - Segment {seg['segment_index']}: {seg['distance_km']} km")
            print(f"       De [{seg['from'][0]:.6f}, {seg['from'][1]:.6f}]")
            print(f"       A  [{seg['to'][0]:.6f}, {seg['to'][1]:.6f}]")

    # Sauvegarder le rapport
    report = {
        'timestamp': '2025-01-13',
        'threshold_km': 5.0,
        'total_problematic_routes': len(problematic_routes),
        'routes': problematic_routes
    }

    with open('straight_segments_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n\n[SAVE] Rapport sauvegarde dans: straight_segments_report.json")

    # Recommandations
    print("\n\nRECOMMANDATIONS")
    print("-" * 60)
    print("1. Routes a corriger prioritairement:")
    for route in problematic_routes[:5]:
        print(f"   - {route['name']} (OSM: {route['osm_id']})")
        print(f"     {route['num_long_segments']} segments > 5km a ameliorer")

    print("\n2. Methodes de correction:")
    print("   a) Editer dans JOSM (Java OpenStreetMap Editor)")
    print("   b) Suivre le trace satellite reel")
    print("   c) Ajouter waypoints aux changements de cap")
    print("   d) Respecter les chenaux de navigation")

    print("\n3. Sources pour traces realistes:")
    print("   - Images satellite (Google Earth, Bing)")
    print("   - Donnees AIS (Marine Traffic)")
    print("   - Cartes marines SHOM")

    print("\n" + "=" * 60)
    print("[OK] Analyse terminee !")

if __name__ == '__main__':
    main()
