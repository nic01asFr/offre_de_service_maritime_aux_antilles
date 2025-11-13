#!/usr/bin/env python3
"""
Enrichit compagnies_enriched.json avec classification des services
Ajoute: type_service, usage, transport_vehicules pour chaque route
"""

import json

def classify_service(route_name, operator_name=""):
    """Détermine le type de service basé sur le nom et opérateur"""
    name_lower = route_name.lower()
    op_lower = operator_name.lower()

    # Navettes urbaines
    if 'pointe du bout' in name_lower or 'anse mitan' in name_lower or 'trois ilets' in op_lower or 'blue lines' in op_lower:
        return {
            'type_service': 'navette_urbaine',
            'usage': 'urbain',
            'transport_vehicules': False
        }

    # Routes internationales
    if any(dest in name_lower for dest in ['dominique', 'sainte-lucie', 'martinique', 'guadeloupe', 'saint-martin', 'anguilla']):
        # Check si c'est entre îles françaises ou vraiment international
        if ('martinique' in name_lower and 'guadeloupe' in name_lower) or \
           ('fort-de-france' in name_lower and 'pitre' in name_lower):
            return {
                'type_service': 'passager',
                'usage': 'regional',
                'transport_vehicules': True  # FRS Express transporte véhicules
            }
        return {
            'type_service': 'passager',
            'usage': 'international',
            'transport_vehicules': False
        }

    # Routes locales vers dépendances
    if any(dest in name_lower for dest in ['saintes', 'marie-galante', 'desirade']):
        return {
            'type_service': 'passager',
            'usage': 'local',
            'transport_vehicules': False
        }

    # Saint-Barthélemy (loisir/tourisme)
    if 'barth' in name_lower or 'gustavia' in name_lower:
        return {
            'type_service': 'loisir',
            'usage': 'regional',
            'transport_vehicules': False
        }

    # Default
    return {
        'type_service': 'passager',
        'usage': 'regional',
        'transport_vehicules': False
    }

def main():
    print("Enrichissement avec classification des services...")

    with open('compagnies_enriched.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Parcourir toutes les compagnies
    for compagnie in data['compagnies']:
        # Classification compagnie
        if compagnie['id'] == 'blue-lines':
            compagnie['type_service'] = 'navette_urbaine'
            compagnie['usage'] = 'urbain'
        elif compagnie['id'] in ['ctm-deher', 'karuferry', 'comadile']:
            compagnie['type_service'] = 'passager'
            compagnie['usage'] = 'local'
        elif compagnie['id'] in ['frs-express', 'val-ferry']:
            compagnie['type_service'] = 'mixte'
            compagnie['usage'] = 'regional'
        else:
            compagnie['type_service'] = 'passager'
            compagnie['usage'] = 'regional'

        # Classification routes
        for route in compagnie.get('routes', []):
            classification = classify_service(route['nom'], compagnie['nom'])
            route.update(classification)

            # Ajustements spécifiques
            if compagnie['id'] == 'frs-express':
                # FRS Express transporte véhicules sur certaines routes
                if 'martinique' in route['nom'].lower() and 'guadeloupe' in route['nom'].lower():
                    route['transport_vehicules'] = True

            if compagnie['id'] == 'comadile':
                # Comadile service essentiel La Désirade
                if 'desirade' in route['nom'].lower():
                    route['services'] = route.get('services', [])
                    if 'Service essentiel' not in route['services']:
                        route['services'].append('Service essentiel')

    # Ajouter légende des classifications
    data['classifications'] = {
        'type_service': {
            'passager': 'Transport de passagers uniquement',
            'fret': 'Transport de marchandises',
            'mixte': 'Passagers et véhicules/fret',
            'loisir': 'Excursions touristiques',
            'navette_urbaine': 'Navette quotidienne courte distance'
        },
        'usage': {
            'local': 'Liaisons internes département (< 30 km)',
            'regional': 'Liaisons inter-îles Antilles (30-100 km)',
            'international': 'Liaisons internationales (> 100 km ou hors territoire français)',
            'urbain': 'Navettes urbaines quotidiennes (< 10 km)'
        }
    }

    # Statistiques
    stats = {
        'passager': 0,
        'mixte': 0,
        'loisir': 0,
        'navette_urbaine': 0,
        'fret': 0
    }

    for comp in data['compagnies']:
        stats[comp.get('type_service', 'passager')] += 1

    print("\nClassification des compagnies:")
    for service_type, count in stats.items():
        if count > 0:
            print(f"  {service_type}: {count} compagnies")

    # Sauvegarder
    with open('compagnies_enriched.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n[OK] Fichier mis a jour: compagnies_enriched.json")
    print("Classifications ajoutees: type_service, usage, transport_vehicules")

if __name__ == '__main__':
    main()
