#!/usr/bin/env python3
"""
Script pour corriger tous les liens de navigation dans les modules HTML
"""

import os
import re

# Mapping des liens incorrects vers les liens corrects
LINK_CORRECTIONS = {
    'page_accueil_amelioree.html': 'index.html',
    'chantier.html': '#',
    'planning.html': 'planning_booster.html',
    'tableau_bord_financier.html': '#',
    'module_reunion_ameliore.html': 'module_reunion_moderne.html',
    'module_equipe_ameliore.html': 'module_equipe_modifie.html',
    'integration_travaux_chantier.html': 'module_travaux_materiaux_corrige.html'
}

def fix_navigation_links():
    """Corrige tous les liens de navigation dans les fichiers HTML"""
    
    html_files = [
        'module_equipe_modifie.html',
        'module_reunion_moderne.html', 
        'module_travaux_materiaux_corrige.html',
        'planning_booster.html',
        'synthese_booster.html'
    ]
    
    corrections_made = 0
    
    for filename in html_files:
        if not os.path.exists(filename):
            print(f"⚠️  Fichier non trouvé: {filename}")
            continue
            
        print(f"🔧 Correction des liens dans {filename}...")
        
        # Lire le fichier
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Appliquer les corrections
        for old_link, new_link in LINK_CORRECTIONS.items():
            if old_link in content:
                content = content.replace(f'href="{old_link}"', f'href="{new_link}"')
                content = content.replace(f"href='{old_link}'", f"href='{new_link}'")
                content = content.replace(f"navigateTo('{old_link}')", f"navigateTo('{new_link}')")
                content = content.replace(f'navigateTo("{old_link}")', f'navigateTo("{new_link}")')
                content = content.replace(f"window.location.href = '{old_link}'", f"window.location.href = '{new_link}'")
                content = content.replace(f'window.location.href = "{old_link}"', f'window.location.href = "{new_link}"')
                print(f"   ✅ Corrigé: {old_link} → {new_link}")
                corrections_made += 1
        
        # Sauvegarder si des modifications ont été faites
        if content != original_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   💾 Fichier sauvegardé: {filename}")
        else:
            print(f"   ℹ️  Aucune correction nécessaire dans {filename}")
    
    print(f"\n🎉 Correction terminée! {corrections_made} liens corrigés au total.")

def add_missing_navigation():
    """Ajoute la navigation manquante dans les modules qui n'en ont pas"""
    
    navigation_html = '''
            <li><a href="index.html">🏠 Accueil</a></li>
            <li><a href="#">🏗️ Nouveau Chantier</a></li>
            <li><a href="planning_booster.html">📅 Planning</a></li>
            <li><a href="#">💰 Analyse Financière</a></li>
            <li><a href="module_reunion_moderne.html">🗓️ Réunions</a></li>
            <li><a href="module_equipe_modifie.html">👥 Équipe</a></li>
            <li><a href="module_travaux_materiaux_corrige.html">🔧 Travaux & Matériaux</a></li>
            <li><a href="synthese_booster.html">📊 Synthèse Globale</a></li>
    '''
    
    files_to_check = ['module_reunion_moderne.html']
    
    for filename in files_to_check:
        if not os.path.exists(filename):
            continue
            
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si la navigation complète existe
        if 'Synthèse Globale' not in content:
            print(f"🔧 Ajout de la navigation complète dans {filename}...")
            
            # Trouver et remplacer la section de navigation incomplète
            nav_pattern = r'<li><a href="[^"]*">🏠 Accueil</a></li>.*?</ul>'
            if re.search(nav_pattern, content, re.DOTALL):
                # Remplacer la navigation existante
                content = re.sub(nav_pattern, navigation_html.strip() + '\n        </ul>', content, flags=re.DOTALL)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ Navigation mise à jour dans {filename}")

if __name__ == "__main__":
    print("🚀 Début de la correction des liens de navigation...")
    fix_navigation_links()
    add_missing_navigation()
    print("✨ Correction terminée!")

