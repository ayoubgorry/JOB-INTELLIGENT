# JOB INTELLIGENT - Plateforme d'Analyse des Offres d'Emploi Data

![Status](https://img.shields.io/badge/Status-Active-green) ![Version](https://img.shields.io/badge/Version-1.0-blue)

**Plateforme intégrée de Data Engineering et Business Intelligence pour l'analyse centralisée, la transformation et l'exploitation de plus de 131 000 offres d'emploi provenant de LinkedIn dans le secteur Data.**

---

## Table des Matières

- [Vue d'Ensemble](#vue-densemble)
- [Objectifs du Projet](#objectifs-du-projet)
- [Architecture Générale](#architecture-générale)
- [Structure des Répertoires](#structure-des-répertoires)
- [Installation et Configuration](#installation-et-configuration)
- [Utilisation](#utilisation)
- [Modèles de Données DBT](#modèles-de-données-dbt)
- [Dashboards Power BI](#dashboards-power-bi)
- [Requêtes d'Exploration](#requêtes-dexploration)
- [Maintenance et Evolution](#maintenance-et-evolution)
- [Support et Dépannage](#support-et-dépannage)

---

## Vue d'Ensemble

Ce projet centralise et analyse les offres d'emploi en secteur Data provenant de LinkedIn. Il fournit une infrastructure analytique complète permettant d'identifier les tendances du marché, les compétences les plus demandées, les localités actives et les opportunités géographiques.

### Points Forts du Projet

- **Pipeline ETL complet** : transformation progressive des données brutes vers des modèles analytiques raffinés
- **Architecture en couches** : séparation claire entre données brutes, transformées et analytiques
- **Tableaux de bord interactifs** : visualisations Power BI pour l'exploration des données
- **Scalabilité** : architecture supportant l'ajout de données et de nouvelles sources
- **Fondations pour la recommandation** : infrastructure prête pour un système de matching offres-profils (Phase 2)

### Cadre Technique

- Environnement **100% local** sans infrastructure cloud
- Orchestration par scripts Python et DBT, sans dépendances cloud
- Base de données locale DuckDB pour l'indépendance complète
- Visualisation avec Power BI Desktop

---

## Objectifs du Projet

Ce projet répond à trois objectifs principaux :

### 1. Centralisation des Données
Consolider et organiser les offres d'emploi Data en provenance de LinkedIn dans une structure logique et facilement interrogeable.

### 2. Analyse de Marché
Extraire des insights métier :
- Identification des compétences les plus demandées
- Analyse des tendances géographiques et temporelles
- Distribution des rôles et postes
- Analyse des entreprises recrutant le plus
- Évaluation du télétravail et des types de contrats

### 3. Système de Recommandation Futur
Préparer une fondation technique pour un système de matching offres-profils permettant de recommander automatiquement des offres adaptées aux candidats.

---

## Architecture Générale

Le projet suit l'architecture "medallion" en trois couches, permettant la progression des données du brut au raffiné :

### Flux de Données

```
SOURCE (131K lignes CSV)
    ↓
BRONZE (Copie brute + renommage)
    ↓
SILVER (Nettoyage + transformation)
    ↓
GOLD (Modèles analytiques optimisés)
    ↓
POWER BI (Visualisations)
```

### Détail des Couches

#### Couche BRONZE (Données Brutes)
- **Objectif** : Recevoir et stocker les données source sans modification
- **Contenu** : Copie du fichier CSV source avec renommage minimal
- **Format** : Vue (VIEW) pour minimiser l'espace disque
- **Modèles** :
  - `stg_jobs_raw` : ~131K lignes directement du CSV source

#### Couche SILVER (Données Transformées)
- **Objectif** : Nettoyer, normaliser et enrichir les données
- **Transformations** : 
  - Nettoyage du texte (minuscules, suppression espaces)
  - Normalisation des dates
  - Standardisation des titres de poste (Data Engineer, Data Scientist, etc.)
  - Extraction et normalisation des compétences requises
- **Format** : Tables (TABLE) pour optimiser les jointures
- **Modèles** :
  - `int_jobs_cleaned` : ~131K offres nettoyées
  - `int_job_title_normalization` : ~100K offres avec titres normalisés
  - `int_skills_extraction` : ~500K liens offre-compétence

#### Couche GOLD (Données Analytiques)
- **Objectif** : Fournir des données prêtes pour l'analyse et la visualisation
- **Design** : Schema en étoile (fact/dimension) optimisé pour Power BI
- **Format** : Tables (TABLE) avec indexes sur clés
- **Modèles** :
  - **Dimensions** : temps, entreprises, localisations, compétences
  - **Faits** : offres d'emploi, associations offre-compétence
  - **Agrégations** : données pré-calculées pour les rapports fréquents

---

## Structure des Répertoires

```
job-intelligent/
│
├── README.md                         # Ce document
├── POWER_BI_GUIDE.md                # Guide détaillé pour Power BI
├── final_data.csv                   # Données source (131K lignes)
├── run_pipeline.py                  # Script d'orchestration principal
│
├── data/                            # Données organisées par couche
│   ├── bronze/                      # Couche brute
│   │   └── final_data.csv           # Copie des données source
│   │
│   ├── silver/                      # Couche transformée
│   │   ├── int_jobs_cleaned.csv
│   │   ├── int_job_title_normalization.csv
│   │   └── int_skills_extraction.csv
│   │
│   └── gold/                        # Couche analytique
│       ├── dim_time.csv             # Table dimension temps
│       ├── dim_company.csv          # Table dimension entreprises
│       ├── dim_location.csv         # Table dimension localisations
│       ├── dim_skills.csv           # Table dimension compétences
│       ├── fact_job_offers.csv      # Table de fait principale
│       ├── fact_job_skills.csv      # Table de fait association
│       ├── agg_job_offers_by_category_time.csv
│       ├── agg_skills_demand.csv
│       └── agg_location_analysis.csv
│
└── dbt_project/                     # Projets et modèles DBT
    ├── dbt_project.yml              # Configuration du projet DBT
    ├── profiles.yml                 # Profils de connexion DB
    │
    ├── models/                      # Modèles SQL
    │   ├── bronze/
    │   │   └── stg_jobs_raw.sql
    │   │
    │   ├── silver/
    │   │   ├── int_jobs_cleaned.sql
    │   │   ├── int_job_title_normalization.sql
    │   │   └── int_skills_extraction.sql
    │   │
    │   └── gold/
    │       ├── dim_time.sql
    │       ├── dim_company.sql
    │       ├── dim_location.sql
    │       ├── dim_skills.sql
    │       ├── fact_job_offers.sql
    │       ├── fact_job_skills.sql
    │       ├── agg_job_offers_by_category_time.sql
    │       ├── agg_skills_demand.sql
    │       └── agg_location_analysis.sql
    │
    ├── tests/                       # Tests de validation des données
    ├── macros/                      # Macros DBT réutilisables
    ├── target/                      # Outputs générés (builds)
    └── logs/                        # Journaux d'exécution
```

---

## Installation et Configuration

### Prérequis Système

- **Python** 3.8 ou supérieur
- **Pip** (gestionnaire de paquets Python)
- Minimum 2 GB d'espace disque disponible
- Permissions de lecture/écriture sur le répertoire du projet
- Connexion Internet pour le téléchargement initial des paquets

### Étape 1 : Vérifier l'Environnement

```bash
# Vérifier la version de Python
python --version
# Résultat attendu : Python 3.8.0 ou supérieur

# Vérifier pip
pip --version
# Résultat attendu : pip 20.x ou supérieur
```

### Étape 2 : Installer les Dépendances

```bash
# Installation recommandée dans un environnement virtuel
python -m venv venv
source venv/Scripts/activate  # Windows
# ou source venv/bin/activate  # macOS/Linux

# Installer les paquets requis
pip install dbt-core dbt-duckdb pandas openpyxl numpy
```

### Étape 3 : Initialiser le Projet

```bash
# Naviguer dans le répertoire du projet
cd C:\path\to\job-intelligent

# Initialiser et valider DBT
cd dbt_project
dbt debug

# Résultat attendu : "Connection successful"
```

### Étape 4 : Préparer les Données

```bash
# Vérifier que final_data.csv est présent à la racine du projet
# Le fichier doit contenir les données sources de LinkedIn
dir final_data.csv

# En cas d'absence, remplacer ce fichier par une version plus récente
```

---

## Utilisation

### Approche 1 : Pipeline Automatisé (Recommandée)

Exécution complète du pipeline de transformation en une seule commande :

```bash
cd C:\path\to\job-intelligent
python run_pipeline.py
```

**Ce script automatise** :
1. Vérification des dépendances Python
2. Copie des données source vers la couche Bronze
3. Exécution des transformations DBT (Bronze → Silver → Gold)
4. Validation avec tests DBT
5. Export des tables Gold au format CSV
6. Génération d'un rapport d'exécution détaillé

**Durée estimée** : 5-10 minutes selon la taille des données

**Output attendu** :
- Tables CSV dans `/data/gold/`
- Rapport dans `/reports/execution_report.txt`
- Logs dans `/dbt_project/logs/`

### Approche 2 : Exécution Manuelle par Étapes

Pour un contrôle granulaire ou du debugging :

```bash
cd dbt_project

# 1. Valider la configuration et la connexion DB
dbt debug

# 2. Exécuter les modèles (transformations)
dbt run

# 3. Valider la qualité des données (tests)
dbt test

# 4. Générer et consulter la documentation
dbt docs generate
dbt docs serve  # Ouvre http://localhost:8000
```

### Approche 3 : Exécution Sélective

Pour exécuter uniquement certains modèles ou couches :

```bash
# Exécuter uniquement la couche Silver
dbt run --select path:models/silver

# Exécuter un modèle spécifique
dbt run --select int_jobs_cleaned

# Exécuter un modèle et ses dépendances
dbt run --select fact_job_offers+

# Rafraîchir complètement (supprimer et recréer)
dbt run --full-refresh
```

---

## Modèles de Données DBT

### Couche BRONZE

| Modèle | Type | Lignes | Description |
|--------|------|--------|-------------|
| stg_jobs_raw | VIEW | ~131K | Lecture brute du CSV source |

### Couche SILVER

| Modèle | Type | Lignes | Description |
|--------|------|--------|-------------|
| int_jobs_cleaned | TABLE | ~131K | Nettoyage du texte et dates |
| int_job_title_normalization | TABLE | ~100K | Normalisation des titres de poste |
| int_skills_extraction | TABLE | ~500K | Extraction des compétences par offre |

### Couche GOLD - Tables de Dimension

| Modèle | Type | Lignes | Clé Primaire | Utilité |
|--------|------|--------|--------------|---------|
| dim_time | TABLE | ~2K | date_id | Analyse temporelle |
| dim_company | TABLE | ~5K | company_id | Analyse par entreprise |
| dim_location | TABLE | ~3K | location_id | Analyse géographique |
| dim_skills | TABLE | ~30 | skill_id | Analyse des compétences |

### Couche GOLD - Tables de Fait

| Modèle | Type | Lignes | Description |
|--------|------|--------|-------------|
| fact_job_offers | TABLE | ~100K | Offres d'emploi avec contexte |
| fact_job_skills | TABLE | ~500K | Association offre-compétence |

### Couche GOLD - Tables d'Agrégation

| Modèle | Type | Description |
|--------|------|-------------|
| agg_job_offers_by_category_time | TABLE | Agrégation temporelle par catégorie |
| agg_skills_demand | TABLE | Demande agrégée de compétences |
| agg_location_analysis | TABLE | Analyse géographique synthétisée |

---

## Dashboards Power BI

### Préparation des Données

1. Ouvrir **Power BI Desktop**
2. Menu : **Fichier → Nouveau**
3. Menu : **Accueil → Obtenir les données → Texte/CSV**
4. Naviguer vers : `C:\path\to\job-intelligent\data\gold\`

### Ordre de Chargement Recommandé

```
1. dim_time.csv          # Dimensions en premier
2. dim_company.csv
3. dim_location.csv
4. dim_skills.csv
5. fact_job_offers.csv   # Tables de fait ensuite
6. fact_job_skills.csv
7. agg_*.csv             # Tables d'agrégation optionnelles
```

### Configuration du Modèle de Données

Créer les relations suivantes dans l'onglet "Modèle" :

| Relation | Cardinality | Type |
|----------|-------------|------|
| fact_job_offers[company_id] → dim_company[company_id] | 1:N | Many-to-One |
| fact_job_offers[location_id] → dim_location[location_id] | 1:N | Many-to-One |
| fact_job_offers[published_date_id] → dim_time[date_id] | 1:N | Many-to-One |
| fact_job_skills[job_offer_id] → fact_job_offers[job_offer_id] | 1:N | Many-to-One |
| fact_job_skills[skill_id] → dim_skills[skill_id] | 1:N | Many-to-One |

Consulter le [POWER_BI_GUIDE.md](POWER_BI_GUIDE.md) pour les dashboards détaillés, mesures DAX et design recommandé.

### Pages de Rapports à Créer

- **Vue d'Ensemble** : Indicateurs clés, tendances générales
- **Analyse par Catégorie d'Emploi** : Détails par rôle
- **Analyse des Compétences** : Top 20 skills, demande
- **Analyse Géographique** : Cartes, répartition par ville
- **Analyse des Entreprises** : Top recruteurs
- **Analytique Avancée** : Heatmaps, corrélations

---

## Requêtes d'Exploration

### Validation des Données SILVER

```sql
-- Nombre total d'offres
SELECT COUNT(*) as total_offers 
FROM silver.int_jobs_cleaned;

-- Distribution par catégorie d'emploi
SELECT 
    job_category,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as percentage
FROM silver.int_job_title_normalization
GROUP BY job_category
ORDER BY count DESC;

-- Top 20 compétences demandées
SELECT 
    skill_name,
    COUNT(*) as demand_count
FROM silver.int_skills_extraction
GROUP BY skill_name
ORDER BY demand_count DESC
LIMIT 20;

-- Distribution temporelle
SELECT 
    DATE_TRUNC('month', published_date) as month,
    COUNT(*) as offers_per_month
FROM silver.int_jobs_cleaned
GROUP BY DATE_TRUNC('month', published_date)
ORDER BY month ASC;
```

### Validation des Données GOLD

```sql
-- Vérifier les comptes dans les tables principales
SELECT 
    'fact_job_offers' as table_name,
    COUNT(*) as row_count
FROM gold.fact_job_offers
UNION ALL
SELECT 'dim_company', COUNT(*) FROM gold.dim_company
UNION ALL
SELECT 'dim_location', COUNT(*) FROM gold.dim_location
UNION ALL
SELECT 'dim_skills', COUNT(*) FROM gold.dim_skills
UNION ALL
SELECT 'fact_job_skills', COUNT(*) FROM gold.fact_job_skills;

-- Top 10 entreprises recrutant
SELECT 
    company_name,
    COUNT(*) as number_of_offers
FROM gold.dim_company dc
INNER JOIN gold.fact_job_offers fjo ON dc.company_id = fjo.company_id
GROUP BY company_name
ORDER BY number_of_offers DESC
LIMIT 10;
```

---

## Maintenance et Evolution

### Mise à Jour des Données

Pour mettre à jour avec un fichier source plus récent :

```bash
# 1. Remplacer final_data.csv par la nouvelle version
cp new_data.csv final_data.csv

# 2. Relancer le pipeline complet
python run_pipeline.py

# 3. Rafraîchir les données dans Power BI
# Menu : Données → Rafraîchir
```

### Ajouter une Nouvelle Compétence

Pour inclure une nouvelle compétence à extraire :

1. Éditer : `dbt_project/models/silver/int_skills_extraction.sql`
2. Ajouter dans la section `UNION ALL` :
   ```sql
   UNION ALL 
   SELECT job_id, 'New Skill', similarity_score
   FROM bronze.stg_jobs_raw
   WHERE description ILIKE '%pattern_keyword%'
   ```
3. Exécuter : `dbt run --select int_skills_extraction`

### Modifier une Normalisation de Titre

Pour ajuster la normalisation des titres de poste :

1. Éditer : `dbt_project/models/silver/int_job_title_normalization.sql`
2. Modifier la clause `CASE WHEN` :
   ```sql
   WHEN job_title_original ILIKE '%pattern%' THEN 'Normalized Category'
   ```
3. Exécuter : `dbt run --select int_job_title_normalization`

---

## Support et Dépannage

### Erreurs Courantes

#### "dbt: command not found"
```bash
# Installation de dbt
pip install dbt-core dbt-duckdb

# Vérification
dbt --version
```

#### "DuckDB ImportError"
```bash
# Réinstaller DuckDB
pip install --upgrade duckdb

# Vérifier la version
python -c "import duckdb; print(duckdb.__version__)"
```

#### "final_data.csv not found"
```bash
# Vérifier la localisation
dir final_data.csv

# Vérifier le chemin dans stg_jobs_raw.sql
# Doit correspondre au chemin réel du fichier
```

#### "Connection Error" lors de dbt debug
```bash
# Vérifier les permissions
# Vérifier que DuckDB est installé
# Réinitialiser : dbt debug --profiles-dir .
```

### Journaux et Debugging

Les journaux détaillés des exécutions se trouvent dans :
```
dbt_project/logs/dbt.log
```

Pour un debugging verbose :
```bash
dbt run --debug
dbt test --debug
```

### Performance

Si l'exécution est lente :
- Vérifier l'espace disque disponible (min 2 GB)
- Réduire temporairement la taille de final_data.csv pour les tests
- Exécuter par couche : `dbt run --select path:models/silver`

---

## Évolutions Futures

Ces fonctionnalités sont prévues pour la Phase 2 :

- Système de recommandation utilisant le machine learning
- API REST pour servir les recommandations
- Alertes automatiques de nouvelles offres matchées
- Dashboard temps réel avec Streamlit
- Intégration directe avec l'API LinkedIn pour la mise à jour quotidienne automatique

---

## Licence et Attribution

**Projet personnel** - Usage libre

---

## Informations Projet

- **Créé** : Janvier 2026
- **Version Actuelle** : 1.0
- **Dernière Mise à Jour** : Janvier 2026
- **Domaine** : Data Engineering & Business Intelligence

---

## Besoin d'Aide ?

Pour toute question ou problème :
1. Consulter le [POWER_BI_GUIDE.md](POWER_BI_GUIDE.md) pour les détails Power BI
2. Vérifier les logs : `dbt_project/logs/`
3. Examiner les tests : `dbt test` pour valider les données

**Analyse heureuse des données !**
