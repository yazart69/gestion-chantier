// Données simulées pour le gestionnaire de chantier V2.2
const CHANTIERS_DATA = {
    "vichy": {
        nom: "VICHY - Rénovation Façade",
        numero: "22341113974",
        statut: "En cours",
        progression: 75,
        budget: 45000,
        equipe: 6,
        joursRestants: 12,
        responsable: "FARID MESSAL",
        dateDebut: "2024-08-15",
        dateFin: "2024-09-15"
    },
    "campenon": {
        nom: "CAMPENON BERNARD - Structure",
        numero: "22441114303",
        statut: "En retard",
        progression: 45,
        budget: 78000,
        equipe: 8,
        joursRestants: 18,
        responsable: "ERTUGRUL YASAR",
        dateDebut: "2024-08-01",
        dateFin: "2024-09-20"
    },
    "pont-chasse": {
        nom: "PONT DE CHASSE - Peinture",
        numero: "2211113275",
        statut: "En cours",
        progression: 60,
        budget: 32000,
        equipe: 4,
        joursRestants: 8,
        responsable: "LOU PIEDIGROSSI",
        dateDebut: "2024-08-20",
        dateFin: "2024-09-10"
    },
    "effia": {
        nom: "EFFIA PARKING - Maintenance",
        numero: "22541114486",
        statut: "Planifié",
        progression: 0,
        budget: 25000,
        equipe: 3,
        joursRestants: 15,
        responsable: "GRANDADAM G",
        dateDebut: "2024-09-05",
        dateFin: "2024-09-25"
    }
};

const EQUIPE_DATA = [
    {
        nom: "FARID MESSAL",
        poste: "Chef de chantier",
        statut: "Disponible",
        experience: 12,
        chantierActuel: "VICHY",
        competences: ["management", "sécurité", "qualité"]
    },
    {
        nom: "ERTUGRUL YASAR",
        poste: "Conducteur de travaux",
        statut: "Disponible",
        experience: 8,
        chantierActuel: "CAMPENON BERNARD",
        competences: ["management", "planning", "commercial"]
    },
    {
        nom: "LOU PIEDIGROSSI",
        poste: "HSE",
        statut: "Disponible",
        experience: 6,
        chantierActuel: "Multi-sites",
        competences: ["sécurité", "environnement", "formation"]
    },
    {
        nom: "A MOHAMED",
        poste: "Chef d'équipe",
        statut: "Disponible",
        experience: 4,
        chantierActuel: "PONT DE CHASSE",
        competences: ["sablage", "peinture", "contrôle"]
    }
];

// Fonctions utilitaires
function formatCurrency(amount) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR',
        minimumFractionDigits: 0
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('fr-FR');
}

function calculateDaysRemaining(endDate) {
    const today = new Date();
    const end = new Date(endDate);
    const diffTime = end - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return Math.max(0, diffDays);
}

// Export pour utilisation dans les modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CHANTIERS_DATA, EQUIPE_DATA, formatCurrency, formatDate, calculateDaysRemaining };
}