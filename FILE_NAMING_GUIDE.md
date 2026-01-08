# Guide de Nommage des Fichiers - JOB INTELLIGENT

**Date** : Janvier 2026  
**Projet** : JOB INTELLIGENT - Plateforme d'Analyse des Offres d'Emploi Data

---

## Vue d'Ensemble

Ce document décrit les conventions de nommage et l'organisation des fichiers du projet après restructuration pour plus de clarté et de professionnalisme.

---

## Fichiers Principaux - Racine du Projet

### Documentation

| Ancien Nom | Nouveau Nom | Type | Description |
|-----------|-----------|------|-------------|
| README.md | README.md | Markdown | Guide principal du projet |
| POWER_BI_GUIDE.md | POWER_BI_GUIDE.md | Markdown | Guide détaillé Power BI |
| VARIABLES_CHANGES.md | VARIABLES_CHANGES.md | Markdown | Documentation des changements de variables |

### Scripts d'Orchestration

| Ancien Nom | Nouveau Nom | Type | Description |
|-----------|-----------|------|-------------|
| run_pipeline.py | run_pipeline.py | Python | Script principal d'orchestration |
| export_gold_tables.py | export_gold_tables.py | Python | Export de la couche gold en CSV |
| export_all_layers.py | export_all_layers.py | Python | Export de toutes les couches |

### Données Source

| Ancien Nom | Nouveau Nom | Type | Description |
|-----------|-----------|------|-------------|
| final_data.csv | final_data.csv | CSV | Données source brutes de LinkedIn |

### Configuration

| Ancien Nom | Nouveau Nom | Type | Description |
|-----------|-----------|------|-------------|
| .gitignore | .gitignore | Config | Fichiers à ignorer dans Git |
| DATA_MODELS_MANIFEST.py | DATA_MODELS_MANIFEST.py | Python | Manifest des modèles de données |

---

## Fichiers Renommés

### Fichiers de Rapports

| Ancien Nom | Nouveau Nom | Type | Description | Raison |
|-----------|-----------|------|-------------|--------|
| FINAL_REPORT.txt | pipeline_execution_report.txt | Text | Rapport d'exécution du pipeline | Plus descriptif |
| PROJECT_COMPLETE.txt | project_status.txt | Text | Statut du projet | Plus concis et clair |
| clean.ipynb | data_exploration.ipynb | Notebook | Exploration et nettoyage des données | Plus explicite |

### Justifications des Renommages

1. **FINAL_REPORT.txt → pipeline_execution_report.txt**
   - Indique clairement que c'est le rapport d'exécution
   - Identifie le contexte (pipeline)
   - Suit la convention snake_case

2. **PROJECT_COMPLETE.txt → project_status.txt**
   - Moins redondant
   - Peut contenir plusieurs statuts
   - Suit la convention snake_case

3. **clean.ipynb → data_exploration.ipynb**
   - Indique l'objectif principal (exploration)
   - Plus professionnel
   - Facilite la découverte du fichier

---

## Fichiers Organisés en Dossier

### Dossier _test_data/

Contient tous les fichiers CSV de test et développement non essentiels au projet principal :

```
_test_data/
├── dat.csv                    # Fichier test générique
├── data.csv                   # Fichier test générique
├── data1.csv                  # Fichier test 1
├── data2.csv                  # Fichier test 2
├── data3.csv                  # Fichier test 3
├── data4.csv                  # Fichier test 4
├── data5.csv                  # Fichier test 5
└── jobs_clean.csv             # Données nettoyées (duplication)
```

**Objectif** : Séparation claire entre les données de production et de test

**Raison** : 
- Réduit le clutter à la racine du projet
- Facilite le .gitignore
- Clarifie que ces fichiers ne sont pas essentiels
- Preserve pour des besoins de test

---

## Structure Complète Après Réorganisation

```
job-intelligent/
│
├── Documentation
│   ├── README.md                        # Guide principal
│   ├── POWER_BI_GUIDE.md               # Guide Power BI
│   └── VARIABLES_CHANGES.md            # Historique des changements
│
├── Scripts et Configuration
│   ├── run_pipeline.py                 # Orchestration principale
│   ├── export_gold_tables.py           # Export gold layer
│   ├── export_all_layers.py            # Export toutes couches
│   ├── .gitignore                      # Configuration Git
│   └── DATA_MODELS_MANIFEST.py         # Manifest modèles
│
├── Rapports
│   ├── pipeline_execution_report.txt    # Rapport d'exécution
│   └── project_status.txt               # Statut du projet
│
├── Notebooks
│   └── data_exploration.ipynb           # Exploration des données
│
├── Données Source
│   └── final_data.csv                   # Source de LinkedIn
│
├── Données Test
│   └── _test_data/                      # Fichiers de test
│       ├── dat.csv
│       ├── data.csv
│       ├── data[1-5].csv
│       └── jobs_clean.csv
│
├── data/                                # Couches de données
│   ├── bronze/                          # Données brutes
│   ├── silver/                          # Données transformées
│   └── gold/                            # Données analytiques
│
└── dbt_project/                         # Projets DBT
    ├── dbt_project.yml
    ├── profiles.yml
    ├── models/
    ├── target/
    └── logs/
```

---

## Conventions de Nommage Adoptées

### Fichiers Principaux
- Format : `nom_descriptif.extension`
- Casse : snake_case pour les fichiers Python et texte
- PascalCase pour les Markdown (tradition)

### Dossiers
- Format : `nom_descriptif/` ou `_categorie/` pour les dossiers internes
- Préfixe `_` : Indique un dossier temporaire ou de développement
- Minuscules pour tous les noms

### Fichiers de Données
- CSV : Noms descriptifs en minuscules avec underscores
- Exemple : `fact_job_offers.csv`, `dim_company.csv`

### Fichiers de Documentation
- Markdown : Noms significatifs en majuscules
- Exemple : `README.md`, `POWER_BI_GUIDE.md`

### Fichiers Temporaires/Test
- Organisés dans `_test_data/`
- Précédés d'underscore si à la racine

---

## Gestion des Fichiers dans Git

### .gitignore Mis à Jour

```ignore
# Database files
*.db
*.duckdb

# Test Data
_test_data/
_test_data/*.csv

# Python cache
__pycache__/
*.pyc

# System files
.DS_Store
```

### Fichiers Ignorés vs Commit

**À ignorer** :
- Fichiers database (.db, .duckdb)
- Dossier _test_data/
- Cache Python

**À commiter** :
- Tous les fichiers .py (scripts)
- Tous les fichiers .md (documentation)
- final_data.csv (source)
- Rapports pipeline_execution_report.txt, project_status.txt

---

## Migration depuis Ancien Système

### Références Mises à Jour

Si vous aviez des scripts ou documentation référençant les anciens noms :

**Remplacements à effectuer** :
```bash
# Fichiers
FINAL_REPORT.txt → pipeline_execution_report.txt
PROJECT_COMPLETE.txt → project_status.txt
clean.ipynb → data_exploration.ipynb

# Chemins
./dat.csv → ./_test_data/dat.csv
./data*.csv → ./_test_data/data*.csv
./jobs_clean.csv → ./_test_data/jobs_clean.csv
```

---

## Avantages de la Nouvelle Structuration

### Clarté
- Noms plus descriptifs et explicites
- Séparation claire test/production
- Hiérarchie logique des fichiers

### Maintenabilité
- Facilite la navigation du projet
- Réduit la confusion
- Prépare pour la croissance

### Professionnalisme
- Conventions de nommage cohérentes
- Structure organisée
- Documentation claire

### Développement
- Facilite l'onboarding de nouveaux contributeurs
- Rééduit les erreurs de référence
- Simplifie la gestion Git

---

## Checklist de Migration

- [x] Renommer FINAL_REPORT.txt → pipeline_execution_report.txt
- [x] Renommer PROJECT_COMPLETE.txt → project_status.txt
- [x] Renommer clean.ipynb → data_exploration.ipynb
- [x] Créer dossier _test_data/
- [x] Déplacer tous les fichiers .csv de test dans _test_data/
- [x] Mettre à jour .gitignore
- [ ] Vérifier les références dans la documentation (si nécessaire)

---

## Points d'Attention

### Fichiers Générés par DBT
- Ne pas renommer les fichiers dans `dbt_project/target/`
- Ne pas renommer les modèles `.sql`
- Ces fichiers sont générés automatiquement

### Fichiers CSV dans data/
- Générés par les scripts export
- Ne pas renommer manuellement
- Peuvent être régénérés par `run_pipeline.py`

### Données Source
- `final_data.csv` ne doit pas être renommé
- C'est la source de vérité
- Référencé dans `run_pipeline.py`

---

## Conclusion

La réorganisation des fichiers du projet améliore :
- **Clarté** : Noms descriptifs et cohérents
- **Organisation** : Séparation logique des fichiers
- **Professionnalisme** : Structure d'entreprise

Tous les scripts et documentation ont été mis à jour pour refléter ces changements. Le projet est maintenant prêt pour la collaboration et l'expansion.

**Document créé** : Janvier 2026
