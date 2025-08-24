// Fichier : database.js (Version finale)

const DB = {
    init: function() {
        if (!localStorage.getItem('chantiers')) {
            localStorage.setItem('chantiers', JSON.stringify([
                { id: 1661346000001, name: 'Rénovation Usine Lyon', budgetInitialHeures: 250, devisValide: 55000, budgetMO: 24000, budgetFournitures: 12000, budgetLocations: 3000, budgetST: 0 },
                { id: 1661346000002, name: 'Chantier Naval - La Ciotat', budgetInitialHeures: 1800, devisValide: 210000, budgetMO: 90000, budgetFournitures: 40000, budgetLocations: 15000, budgetST: 25000 },
            ]));
        }
        if (!localStorage.getItem('equipe')) {
            localStorage.setItem('equipe', JSON.stringify([
                 { id: 1, firstName: 'Farid', lastName: 'MESSAL', role: 'chef-chantier' },
                 { id: 2, firstName: 'Loic', lastName: 'ANTUNEZ', role: 'chef-equipe' },
            ]));
        }
        // Ajout de tâches d'exemple pour le chantier 1
        if (!localStorage.getItem('planning')) {
            const initialPlanning = {
                "1661346000001": [
                    { id: 1, nom: 'Démarrage & Préparation', responsable: 'Conducteur de travaux', dateDebut: '2025-08-21', heuresHomme: 42.5, operateurs: 1, duree: 5, progression: 100, statut: 'termine' },
                    { id: 2, nom: 'Sablage Zone A', responsable: 'Equipe operateurs', dateDebut: '2025-08-28', heuresHomme: 119, operateurs: 2, duree: 7, progression: 50, statut: 'en-cours' },
                    { id: 3, nom: 'Peinture Zone A', responsable: 'Chef atelier St Maurice', dateDebut: '2025-09-08', heuresHomme: 85, operateurs: 1, duree: 10, progression: 0, statut: 'planifie' },
                ]
            };
            localStorage.setItem('planning', JSON.stringify(initialPlanning));
        }
    },
    getChantiers: function() { return JSON.parse(localStorage.getItem('chantiers')) || []; },
    getChantierById: function(id) { return this.getChantiers().find(c => c.id == id); },
    getEquipe: function() { return JSON.parse(localStorage.getItem('equipe')) || []; },
    getPlanningForChantier: function(chantierId) {
        const allPlanning = JSON.parse(localStorage.getItem('planning')) || {};
        return allPlanning[chantierId] || [];
    },
    savePlanningForChantier: function(chantierId, tasks) {
        const allPlanning = JSON.parse(localStorage.getItem('planning')) || {};
        allPlanning[chantierId] = tasks.map(t => {
            // S'assurer que les dates sont stockées dans un format standard
            if (t.dateDebut instanceof Date) {
                t.dateDebut = t.dateDebut.toISOString().split('T')[0];
            }
            return t;
        });
        localStorage.setItem('planning', JSON.stringify(allPlanning));
    }
};
DB.init();