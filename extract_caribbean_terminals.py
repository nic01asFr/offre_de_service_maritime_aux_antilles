#!/usr/bin/env python3
"""
Extrait les embarcadères des Antilles françaises ET leurs destinations régionales
Inclut: Dominique, Sainte-Lucie, Sint Maarten, Anguilla, Saba, Saint-Kitts, etc.
"""

import json

def is_in_caribbean_region(lat: float, lon: float) -> bool:
    """Vérifie si les coordonnées sont dans la région Caraïbes concernée"""
    # Zone élargie pour toutes les destinations
    # Guadeloupe: lat 15.8-16.5, lon -61.8 à -61.0
    # Martinique: lat 14.3-14.9, lon -61.3 à -60.8
    # Saint-Martin/Sint Maarten/Anguilla: lat 17.8-18.3, lon -63.3 à -62.8
    # Dominique: lat 15.2-15.7, lon -61.5 à -61.2
    # Sainte-Lucie: lat 13.7-14.2, lon -61.1 à -60.8
    # Saba/Statia: lat 17.4-17.7, lon -63.3 à -62.9
    # Saint-Kitts: lat 17.1-17.5, lon -62.9 à -62.5

    # Zone globale englobante: lat 13.5-18.5, lon -63.5 à -60.5
    if 13.5 <= lat <= 18.5 and -63.5 <= lon <= -60.5:
        return True
    return False

def main():
    print("Extraction des embarcaderes - Antilles et destinations regionales...")

    with open('ferry_terminals_osm.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Filtrer les embarcadères
    caribbean_terminals = [
        t for t in data['terminals']
        if is_in_caribbean_region(t['lat'], t['lon'])
    ]

    print(f"Total embarcaderes OSM: {len(data['terminals'])}")
    print(f"Embarcaderes Antilles + destinations: {len(caribbean_terminals)}")

    # Grouper par zone géographique
    zones_detail = {}
    for t in caribbean_terminals:
        lat, lon = t['lat'], t['lon']

        # Identifier la zone
        if 15.8 <= lat <= 16.5 and -61.8 <= lon <= -61.0:
            zone = "Guadeloupe"
        elif 14.3 <= lat <= 14.9 and -61.3 <= lon <= -60.8:
            zone = "Martinique"
        elif 17.8 <= lat <= 18.3 and -63.3 <= lon <= -62.8:
            zone = "Saint-Martin/Anguilla"
        elif 15.2 <= lat <= 15.7 and -61.5 <= lon <= -61.2:
            zone = "Dominique"
        elif 13.7 <= lat <= 14.2 and -61.1 <= lon <= -60.8:
            zone = "Sainte-Lucie"
        elif 17.4 <= lat <= 17.7 and -63.3 <= lon <= -62.9:
            zone = "Saba/Statia"
        elif 17.1 <= lat <= 17.5 and -62.9 <= lon <= -62.5:
            zone = "Saint-Kitts"
        else:
            zone = "Autres Caraibes"

        if zone not in zones_detail:
            zones_detail[zone] = []
        zones_detail[zone].append(t)

    # Afficher par zone
    print("\n*** REPARTITION PAR ZONE ***")
    print("-" * 60)
    for zone, terminals in sorted(zones_detail.items(), key=lambda x: -len(x[1])):
        print(f"{zone}: {len(terminals)} embarcaderes")

    # Sauvegarder
    output = {
        'timestamp': '2025-01-13',
        'total': len(caribbean_terminals),
        'by_zone': {zone: len(terms) for zone, terms in zones_detail.items()},
        'terminals': caribbean_terminals
    }

    with open('caribbean_ferry_terminals.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Afficher les principaux embarcadères nommés
    print("\n*** EMBARCADERES PRINCIPAUX (avec nom) ***")
    print("-" * 60)
    named = [t for t in caribbean_terminals if t['name'] != 'Sans nom']
    for i, t in enumerate(named[:30], 1):
        try:
            name = t['name'].encode('ascii', 'replace').decode('ascii')
        except:
            name = "[encodage]"
        # Trouver la zone
        lat, lon = t['lat'], t['lon']
        if 15.8 <= lat <= 16.5 and -61.8 <= lon <= -61.0:
            zone_str = "Guadeloupe"
        elif 14.3 <= lat <= 14.9 and -61.3 <= lon <= -60.8:
            zone_str = "Martinique"
        elif 17.8 <= lat <= 18.3 and -63.3 <= lon <= -62.8:
            zone_str = "St-Martin/Anguilla"
        elif 15.2 <= lat <= 15.7 and -61.5 <= lon <= -61.2:
            zone_str = "Dominique"
        elif 13.7 <= lat <= 14.2 and -61.1 <= lon <= -60.8:
            zone_str = "Sainte-Lucie"
        else:
            zone_str = "Autre"

        print(f"{i}. {name}")
        print(f"   {zone_str} - ({lat:.6f}, {lon:.6f})")

    print(f"\n\n[OK] Sauvegarde dans: caribbean_ferry_terminals.json")
    print(f"Total: {len(caribbean_terminals)} embarcaderes")

if __name__ == '__main__':
    main()
