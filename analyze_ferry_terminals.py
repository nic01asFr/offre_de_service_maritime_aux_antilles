#!/usr/bin/env python3
"""
Analyse les embarcadères (ferry terminals) depuis OpenStreetMap
Compare avec les positions actuelles des ports dans le code
Identifie les embarcadères précis et génère un rapport
"""

import json
import math
import requests
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

def query_overpass_ferry_terminals(bbox: str) -> Dict:
    """
    Interroge Overpass API pour récupérer les embarcadères
    bbox format: "south,west,north,east"
    """
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Requête Overpass pour ferry terminals et ports
    overpass_query = f"""
    [out:json][timeout:60];
    (
      node["amenity"="ferry_terminal"]({bbox});
      node["public_transport"="stop_position"]["ferry"="yes"]({bbox});
      node["leisure"="slipway"]["ferry"="yes"]({bbox});
      way["amenity"="ferry_terminal"]({bbox});
    );
    out body center;
    >;
    out skel qt;
    """

    print(f"Interrogation Overpass API pour bbox: {bbox}")
    try:
        response = requests.post(overpass_url, data={'data': overpass_query}, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erreur lors de la requete Overpass: {e}")
        return {"elements": []}

def main():
    print("Analyse des embarcaderes (ferry terminals) OSM...")
    print("=" * 60)

    # Zones d'intérêt (bbox: south,west,north,east)
    zones = {
        "Guadeloupe": "15.8,- 61.8,16.5,-61.0",
        "Martinique": "14.3,-61.3,14.9,-60.8",
        "Saint-Martin": "17.8,-63.2,18.2,-62.8"
    }

    all_terminals = []

    for zone_name, bbox in zones.items():
        print(f"\n>>> Recherche dans zone: {zone_name}")
        data = query_overpass_ferry_terminals(bbox)

        terminals_in_zone = []
        for element in data.get('elements', []):
            if element['type'] == 'node':
                lat = element.get('lat')
                lon = element.get('lon')
            elif element['type'] == 'way' and 'center' in element:
                lat = element['center'].get('lat')
                lon = element['center'].get('lon')
            else:
                continue

            tags = element.get('tags', {})
            terminal = {
                'zone': zone_name,
                'osm_type': element['type'],
                'osm_id': element['id'],
                'lat': lat,
                'lon': lon,
                'name': tags.get('name', 'Sans nom'),
                'amenity': tags.get('amenity', ''),
                'public_transport': tags.get('public_transport', ''),
                'operator': tags.get('operator', 'Non specifie'),
                'ferry': tags.get('ferry', ''),
                'wheelchair': tags.get('wheelchair', '')
            }
            terminals_in_zone.append(terminal)
            all_terminals.append(terminal)

        print(f"   Trouves: {len(terminals_in_zone)} embarcaderes")

    print(f"\n*** TOTAL: {len(all_terminals)} embarcaderes dans OSM ***\n")

    # Afficher les embarcadères trouvés (top 20)
    print("\n*** EMBARCADERES TROUVES DANS OSM (Top 20) ***")
    print("-" * 60)

    for i, terminal in enumerate(all_terminals[:20], 1):
        try:
            name = terminal['name'].encode('ascii', 'replace').decode('ascii')
            operator = terminal['operator'].encode('ascii', 'replace').decode('ascii')
            print(f"\n{i}. {name}")
            print(f"   Zone: {terminal['zone']}")
            print(f"   Coordonnees: {terminal['lat']:.6f}, {terminal['lon']:.6f}")
            if operator != 'Non specifie':
                print(f"   Operateur: {operator}")
            print(f"   OSM: {terminal['osm_type']}/{terminal['osm_id']}")
        except Exception as e:
            print(f"\n{i}. [Erreur encodage]")
            continue

    # Sauvegarder les résultats
    output = {
        'timestamp': '2025-01-13',
        'total_terminals': len(all_terminals),
        'by_zone': {
            zone: len([t for t in all_terminals if t['zone'] == zone])
            for zone in zones.keys()
        },
        'terminals': all_terminals
    }

    with open('ferry_terminals_osm.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n\n[SAVE] Donnees sauvegardees dans: ferry_terminals_osm.json")

    # Recommandations
    print("\n\n*** RECOMMANDATIONS ***")
    print("-" * 60)
    print("1. Comparer ces positions OSM avec vos donnees actuelles")
    print("2. Utiliser les coordonnees OSM pour une precision maximale")
    print("3. Enrichir avec les attributs OSM (operateur, accessibilite)")
    print("4. Verifier la presence de tous les embarcaderes essentiels")
    print()
    print("Pour contribuer a OSM:")
    print("- Ajouter les embarcaderes manquants")
    print("- Completer les informations (nom, operateur, horaires)")
    print("- Marquer l'accessibilite PMR (wheelchair=yes/no)")

    print("\n" + "=" * 60)
    print("[OK] Analyse terminee !")

if __name__ == '__main__':
    main()
