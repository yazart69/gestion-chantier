#!/usr/bin/env python3
"""
Script pour mettre à jour la navigation dans tous les modules vers la V2.2
"""

import os
import re

# Nouveau menu latéral unifié
SIDEBAR_HTML = '''    <!-- Sidebar permanent -->
    <nav class="sidebar">
        <div class="sidebar-header">
            <div class="sidebar-logo">
                🏗️ Gestionnaire Chantier
            </div>
            <div class="sidebar-subtitle">
                Équipe 41 - Chasse sur Rhône
            </div>
        </div>
        
        <div class="sidebar-nav">
            <div class="nav-section">
                <div class="nav-section-title">Principal</div>
                <a href="index_v2.2.html" class="nav-item{active_home}">
                    <span class="icon">🏠</span>
                    Tableau de Bord
                </a>
                <a href="planning_booster.html" class="nav-item{active_planning}">
                    <span class="icon">📅</span>
                    Planning
                    <span class="badge">3</span>
                </a>
                <a href="pointage_booster.html" class="nav-item{active_pointage}">
                    <span class="icon">⏰</span>
                    Pointage
                </a>
            </div>
            
            <div class="nav-section">
                <div class="nav-section-title">Gestion</div>
                <a href="module_equipe_modifie.html" class="nav-item{active_equipe}">
                    <span class="icon">👥</span>
                    Équipe
                </a>
                <a href="module_travaux_materiaux_corrige.html" class="nav-item{active_travaux}">
                    <span class="icon">🔧</span>
                    Travaux & Matériaux
                </a>
                <a href="module_reunion_moderne.html" class="nav-item{active_reunion}">
                    <span class="icon">🗓️</span>
                    Réunions
                    <span class="badge">2</span>
                </a>
            </div>
            
            <div class="nav-section">
                <div class="nav-section-title">Analyse</div>
                <a href="#" class="nav-item" onclick="alert('Module en développement')">
                    <span class="icon">💰</span>
                    Finances
                </a>
                <a href="#" class="nav-item" onclick="alert('Module en développement')">
                    <span class="icon">📊</span>
                    Rapports
                </a>
                <a href="#" class="nav-item" onclick="alert('Module en développement')">
                    <span class="icon">⚙️</span>
                    Paramètres
                </a>
            </div>
        </div>
    </nav>'''

# CSS pour le sidebar
SIDEBAR_CSS = '''        /* Sidebar permanent */
        .sidebar {
            position: fixed;
            top: 0;
            left: 0;
            width: var(--sidebar-width);
            height: 100vh;
            background: linear-gradient(180deg, var(--primary-red), var(--primary-orange));
            color: white;
            z-index: 1000;
            overflow-y: auto;
            transition: transform 0.3s ease;
        }

        .sidebar-header {
            padding: 2rem 1.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
        }

        .sidebar-logo {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }

        .sidebar-subtitle {
            font-size: 0.9rem;
            opacity: 0.8;
        }

        .sidebar-nav {
            padding: 1rem 0;
        }

        .nav-section {
            margin-bottom: 2rem;
        }

        .nav-section-title {
            padding: 0 1.5rem 0.5rem;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            opacity: 0.7;
        }

        .nav-item {
            display: block;
            padding: 0.75rem 1.5rem;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
            position: relative;
        }

        .nav-item:hover {
            background: rgba(255, 255, 255, 0.1);
            border-left-color: white;
            transform: translateX(5px);
        }

        .nav-item.active {
            background: rgba(255, 255, 255, 0.15);
            border-left-color: white;
            font-weight: 600;
        }

        .nav-item .icon {
            display: inline-block;
            width: 1.5rem;
            margin-right: 0.75rem;
            text-align: center;
        }

        .nav-item .badge {
            position: absolute;
            right: 1rem;
            top: 50%;
            transform: translateY(-50%);
            background: var(--danger);
            color: white;
            font-size: 0.7rem;
            padding: 0.2rem 0.5rem;
            border-radius: 1rem;
            min-width: 1.2rem;
            text-align: center;
        }'''

def update_module_navigation():
    """Met à jour la navigation dans tous les modules"""
    
    modules = {
        'module_equipe_modifie.html': 'equipe',
        'module_reunion_moderne.html': 'reunion', 
        'module_travaux_materiaux_corrige.html': 'travaux',
        'planning_booster.html': 'planning',
        'synthese_booster.html': 'synthese'
    }
    
    for filename, active_page in modules.items():
        if not os.path.exists(filename):
            print(f"⚠️  Fichier non trouvé: {filename}")
            continue
            
        print(f"🔧 Mise à jour de la navigation dans {filename}...")
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ajouter la variable CSS sidebar-width si elle n'existe pas
        if '--sidebar-width:' not in content:
            content = content.replace(':root {', ':root {\n            --sidebar-width: 280px;')
        
        # Ajouter le CSS du sidebar si il n'existe pas
        if '.sidebar {' not in content:
            # Trouver la fin du CSS existant et ajouter le CSS du sidebar
            css_end = content.find('</style>')
            if css_end != -1:
                content = content[:css_end] + '\n' + SIDEBAR_CSS + '\n        ' + content[css_end:]
        
        # Remplacer l'ancienne sidebar par la nouvelle
        sidebar_pattern = r'<nav class="sidebar">.*?</nav>'
        active_classes = {
            'active_home': ' active' if active_page == 'home' else '',
            'active_planning': ' active' if active_page == 'planning' else '',
            'active_pointage': ' active' if active_page == 'pointage' else '',
            'active_equipe': ' active' if active_page == 'equipe' else '',
            'active_travaux': ' active' if active_page == 'travaux' else '',
            'active_reunion': ' active' if active_page == 'reunion' else ''
        }
        
        new_sidebar = SIDEBAR_HTML.format(**active_classes)
        
        if re.search(sidebar_pattern, content, re.DOTALL):
            content = re.sub(sidebar_pattern, new_sidebar, content, flags=re.DOTALL)
        else:
            # Si pas de sidebar existante, l'ajouter après <body>
            body_start = content.find('<body>')
            if body_start != -1:
                body_end = content.find('>', body_start) + 1
                content = content[:body_end] + '\n' + new_sidebar + '\n' + content[body_end:]
        
        # Mettre à jour la classe main-content pour tenir compte du sidebar
        if 'margin-left: var(--sidebar-width)' not in content:
            content = content.replace('.main-content {', '.main-content {\n            margin-left: var(--sidebar-width);')
        
        # Sauvegarder
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ Navigation mise à jour dans {filename}")

def remove_synthese_module():
    """Supprime le module synthèse et met à jour les liens"""
    
    if os.path.exists('synthese_booster.html'):
        os.remove('synthese_booster.html')
        print("🗑️  Module synthese_booster.html supprimé")
    
    # Mettre à jour les liens dans tous les fichiers
    files_to_update = ['index_v2.2.html', 'pointage_booster.html', 'module_equipe_modifie.html', 
                       'module_reunion_moderne.html', 'module_travaux_materiaux_corrige.html', 
                       'planning_booster.html']
    
    for filename in files_to_update:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Supprimer les liens vers synthese_booster.html
            content = content.replace('synthese_booster.html', '#')
            content = content.replace('Synthèse Booster', 'Synthèse (bientôt)')
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    print("🚀 Mise à jour de la navigation V2.2...")
    update_module_navigation()
    remove_synthese_module()
    print("✨ Mise à jour terminée!")

