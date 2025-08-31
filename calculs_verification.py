#!/usr/bin/env python3
"""
Script de vérification et optimisation des calculs pour le gestionnaire de chantier
"""

import math
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

class CalculsChantier:
    """Classe pour vérifier et optimiser tous les calculs du gestionnaire de chantier"""
    
    def __init__(self):
        self.prix_materiaux = {
            'peinture_standard': 25.50,  # €/L
            'peinture_premium': 45.80,   # €/L
            'primer': 18.90,             # €/L
            'vernis': 32.40,             # €/L
            'enduit': 12.30,             # €/kg
            'sable': 8.50,               # €/sac 25kg
            'ciment': 15.20,             # €/sac 35kg
            'acier': 850.00,             # €/tonne
            'beton': 120.00,             # €/m³
        }
        
        self.rendements = {
            'peinture': 8.5,    # m²/L
            'primer': 10.0,     # m²/L
            'vernis': 12.0,     # m²/L
            'enduit': 2.5,      # m²/kg
        }
        
        self.coefficients_majoration = {
            'complexite_faible': 1.0,
            'complexite_moyenne': 1.15,
            'complexite_elevee': 1.35,
            'acces_difficile': 1.25,
            'hauteur_importante': 1.40,
            'conditions_meteo': 1.10,
        }

    def calculer_surface_totale(self, surfaces: Dict[str, float]) -> float:
        """Calcule la surface totale en tenant compte des coefficients"""
        surface_brute = sum(surfaces.values())
        
        # Coefficient de perte (chutes, retouches)
        coeff_perte = 1.08
        
        # Coefficient de complexité selon le type de surface
        coeff_complexite = 1.0
        if 'facade' in surfaces:
            coeff_complexite = max(coeff_complexite, 1.15)
        if 'toiture' in surfaces:
            coeff_complexite = max(coeff_complexite, 1.25)
        if 'structure_metallique' in surfaces:
            coeff_complexite = max(coeff_complexite, 1.20)
            
        return round(surface_brute * coeff_perte * coeff_complexite, 2)

    def calculer_quantite_materiau(self, surface: float, type_materiau: str, 
                                 nb_couches: int = 1) -> float:
        """Calcule la quantité de matériau nécessaire"""
        if type_materiau not in self.rendements:
            raise ValueError(f"Type de matériau inconnu: {type_materiau}")
            
        rendement = self.rendements[type_materiau]
        quantite_base = (surface * nb_couches) / rendement
        
        # Marge de sécurité de 5%
        quantite_avec_marge = quantite_base * 1.05
        
        return math.ceil(quantite_avec_marge)

    def calculer_cout_materiau(self, quantite: float, type_materiau: str) -> float:
        """Calcule le coût d'un matériau"""
        if type_materiau not in self.prix_materiaux:
            raise ValueError(f"Prix non défini pour: {type_materiau}")
            
        prix_unitaire = self.prix_materiaux[type_materiau]
        return round(quantite * prix_unitaire, 2)

    def calculer_main_oeuvre(self, surface: float, type_travaux: str, 
                           complexite: str = 'moyenne') -> Dict[str, float]:
        """Calcule les coûts de main d'œuvre"""
        
        # Temps de base par m² selon le type de travaux (en heures)
        temps_base = {
            'peinture_simple': 0.25,
            'peinture_decorative': 0.45,
            'traitement_anticorrosion': 0.35,
            'renovation_complete': 0.60,
            'structure_metallique': 0.40,
        }
        
        if type_travaux not in temps_base:
            type_travaux = 'peinture_simple'
            
        temps_unitaire = temps_base[type_travaux]
        
        # Application du coefficient de complexité
        coeff = self.coefficients_majoration.get(f'complexite_{complexite}', 1.15)
        temps_total = surface * temps_unitaire * coeff
        
        # Coûts horaires
        taux_horaire_ouvrier = 35.50
        taux_horaire_specialiste = 45.80
        
        # Répartition selon le type de travaux
        if 'decorative' in type_travaux or 'anticorrosion' in type_travaux:
            heures_specialiste = temps_total * 0.6
            heures_ouvrier = temps_total * 0.4
        else:
            heures_specialiste = temps_total * 0.3
            heures_ouvrier = temps_total * 0.7
            
        cout_ouvrier = heures_ouvrier * taux_horaire_ouvrier
        cout_specialiste = heures_specialiste * taux_horaire_specialiste
        
        return {
            'heures_ouvrier': round(heures_ouvrier, 2),
            'heures_specialiste': round(heures_specialiste, 2),
            'cout_ouvrier': round(cout_ouvrier, 2),
            'cout_specialiste': round(cout_specialiste, 2),
            'cout_total': round(cout_ouvrier + cout_specialiste, 2),
            'temps_total': round(temps_total, 2)
        }

    def calculer_planning_optimise(self, taches: List[Dict], 
                                 contraintes: Dict = None) -> List[Dict]:
        """Optimise le planning des tâches"""
        if not contraintes:
            contraintes = {
                'heures_par_jour': 8,
                'jours_par_semaine': 5,
                'equipe_size': 4,
                'buffer_meteo': 0.15  # 15% de temps supplémentaire pour météo
            }
            
        planning_optimise = []
        date_debut = datetime.now()
        
        for i, tache in enumerate(taches):
            duree_base = tache.get('duree_heures', 8)
            
            # Application du buffer météo
            duree_avec_buffer = duree_base * (1 + contraintes['buffer_meteo'])
            
            # Calcul du nombre de jours nécessaires
            heures_par_jour = contraintes['heures_par_jour']
            jours_necessaires = math.ceil(duree_avec_buffer / heures_par_jour)
            
            # Calcul des dates en tenant compte des week-ends
            jours_calendaires = jours_necessaires * 7 / contraintes['jours_par_semaine']
            
            date_fin = date_debut + timedelta(days=jours_calendaires)
            
            tache_optimisee = {
                **tache,
                'date_debut': date_debut.strftime('%Y-%m-%d'),
                'date_fin': date_fin.strftime('%Y-%m-%d'),
                'duree_jours': jours_necessaires,
                'duree_avec_buffer': round(duree_avec_buffer, 2),
                'ressources_necessaires': math.ceil(duree_avec_buffer / (jours_necessaires * heures_par_jour))
            }
            
            planning_optimise.append(tache_optimisee)
            date_debut = date_fin + timedelta(days=1)  # 1 jour de battement
            
        return planning_optimise

    def calculer_rentabilite_projet(self, cout_total: float, prix_vente: float, 
                                  duree_jours: int) -> Dict[str, float]:
        """Calcule la rentabilité d'un projet"""
        
        # Coûts indirects (15% du coût total)
        couts_indirects = cout_total * 0.15
        
        # Coût total avec indirects
        cout_total_reel = cout_total + couts_indirects
        
        # Marge brute
        marge_brute = prix_vente - cout_total_reel
        taux_marge = (marge_brute / prix_vente) * 100 if prix_vente > 0 else 0
        
        # Rentabilité par jour
        rentabilite_jour = marge_brute / duree_jours if duree_jours > 0 else 0
        
        # Seuil de rentabilité (marge minimum de 20%)
        prix_seuil = cout_total_reel / 0.8
        
        return {
            'cout_direct': cout_total,
            'cout_indirect': round(couts_indirects, 2),
            'cout_total': round(cout_total_reel, 2),
            'prix_vente': prix_vente,
            'marge_brute': round(marge_brute, 2),
            'taux_marge': round(taux_marge, 2),
            'rentabilite_jour': round(rentabilite_jour, 2),
            'prix_seuil_rentabilite': round(prix_seuil, 2),
            'recommandation': 'Rentable' if taux_marge >= 20 else 'Non rentable'
        }

    def verifier_coherence_donnees(self, donnees: Dict) -> List[str]:
        """Vérifie la cohérence des données saisies"""
        erreurs = []
        
        # Vérification des surfaces
        if 'surfaces' in donnees:
            for nom, surface in donnees['surfaces'].items():
                if surface < 0:
                    erreurs.append(f"Surface négative détectée: {nom} = {surface}")
                if surface > 10000:  # Surface très importante
                    erreurs.append(f"Surface très importante: {nom} = {surface} m² (à vérifier)")
        
        # Vérification des quantités
        if 'materiaux' in donnees:
            for materiau, quantite in donnees['materiaux'].items():
                if quantite < 0:
                    erreurs.append(f"Quantité négative: {materiau} = {quantite}")
        
        # Vérification des dates
        if 'planning' in donnees:
            for tache in donnees['planning']:
                if 'date_debut' in tache and 'date_fin' in tache:
                    debut = datetime.fromisoformat(tache['date_debut'])
                    fin = datetime.fromisoformat(tache['date_fin'])
                    if fin < debut:
                        erreurs.append(f"Date de fin antérieure au début: {tache.get('nom', 'Tâche inconnue')}")
        
        return erreurs

    def generer_rapport_calculs(self, projet: Dict) -> str:
        """Génère un rapport détaillé des calculs"""
        
        rapport = f"""
RAPPORT DE CALCULS - PROJET {projet.get('nom', 'Sans nom')}
{'='*60}

Date de génération: {datetime.now().strftime('%d/%m/%Y %H:%M')}

SURFACES:
---------
"""
        
        if 'surfaces' in projet:
            surface_totale = self.calculer_surface_totale(projet['surfaces'])
            rapport += f"Surface totale calculée: {surface_totale} m²\n"
            
            for nom, surface in projet['surfaces'].items():
                rapport += f"  - {nom}: {surface} m²\n"

        if 'materiaux' in projet:
            rapport += "\nMATÉRIAUX:\n----------\n"
            cout_total_materiaux = 0
            
            for materiau, quantite in projet['materiaux'].items():
                if materiau in self.prix_materiaux:
                    cout = self.calculer_cout_materiau(quantite, materiau)
                    cout_total_materiaux += cout
                    rapport += f"  - {materiau}: {quantite} unités = {cout}€\n"
            
            rapport += f"\nCoût total matériaux: {cout_total_materiaux}€\n"

        if 'main_oeuvre' in projet:
            rapport += "\nMAIN D'ŒUVRE:\n-------------\n"
            mo = projet['main_oeuvre']
            rapport += f"  - Heures ouvrier: {mo.get('heures_ouvrier', 0)}h\n"
            rapport += f"  - Heures spécialiste: {mo.get('heures_specialiste', 0)}h\n"
            rapport += f"  - Coût total: {mo.get('cout_total', 0)}€\n"

        return rapport

def test_calculs():
    """Fonction de test pour vérifier les calculs"""
    calc = CalculsChantier()
    
    print("=== TEST DES CALCULS ===")
    
    # Test 1: Calcul de surface
    surfaces_test = {
        'facade_nord': 150.5,
        'facade_sud': 180.2,
        'toiture': 220.8
    }
    
    surface_totale = calc.calculer_surface_totale(surfaces_test)
    print(f"Surface totale: {surface_totale} m²")
    
    # Test 2: Calcul de matériaux
    quantite_peinture = calc.calculer_quantite_materiau(surface_totale, 'peinture', 2)
    cout_peinture = calc.calculer_cout_materiau(quantite_peinture, 'peinture_standard')
    print(f"Peinture nécessaire: {quantite_peinture}L = {cout_peinture}€")
    
    # Test 3: Main d'œuvre
    mo = calc.calculer_main_oeuvre(surface_totale, 'peinture_simple', 'moyenne')
    print(f"Main d'œuvre: {mo['temps_total']}h = {mo['cout_total']}€")
    
    # Test 4: Rentabilité
    cout_total = cout_peinture + mo['cout_total']
    rentabilite = calc.calculer_rentabilite_projet(cout_total, cout_total * 1.3, 10)
    print(f"Rentabilité: {rentabilite['taux_marge']}% - {rentabilite['recommandation']}")
    
    print("\n=== TESTS TERMINÉS ===")

if __name__ == "__main__":
    test_calculs()

