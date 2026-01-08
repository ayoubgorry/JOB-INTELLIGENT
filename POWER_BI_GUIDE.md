# Guide Complet Power BI - JOB INTELLIGENT

**Guide détaillé pour configurer et exploiter les dashboards Power BI de la plateforme d'analyse des offres d'emploi Data.**

---

## Table des Matières

- [Introduction](#introduction)
- [Préparation des Données](#préparation-des-données)
- [Configuration du Modèle](#configuration-du-modèle)
- [Mesures et Calculs DAX](#mesures-et-calculs-dax)
- [Dashboards Recommandés](#dashboards-recommandés)
- [Slicers et Filtres](#slicers-et-filtres)
- [Mise en Forme](#mise-en-forme)
- [Optimisation des Performances](#optimisation-des-performances)
- [Publication et Partage](#publication-et-partage)
- [Dépannage](#dépannage)

---

## Introduction

### Objectif

Ce guide vous accompagne dans la création d'une solution de visualisation interactive permettant l'analyse complète des offres d'emploi Data avec un ensemble cohérent d'indicateurs clés (KPIs) et de recommandations visuelles.

### Résultat Attendu

Une suite de 6 dashboards interactifs couvrant :
- Vue d'ensemble avec KPIs
- Analyse détaillée par catégorie d'emploi
- Demande et tendance des compétences
- Distribution géographique
- Analyse des entreprises recrutant
- Analytique avancée et correlations

---

## Préparation des Données

### Étape 1 : Importer les Tables Gold

#### 1.1 Ouvrir Power BI Desktop

1. Lancez **Power BI Desktop**
2. Cliquez sur **Fichier → Nouveau**
3. Une interface vierge s'affiche

#### 1.2 Charger les Fichiers CSV

Pour chaque table, procédez comme suit :

1. Menu : **Accueil → Obtenir les données → Texte/CSV**
2. Naviguez vers : `C:\Users\Ayoub Gorry\Desktop\powerbi\jobs-power-bi\data\gold\`
3. Sélectionnez le fichier CSV
4. Cliquez sur **Charger**

#### 1.3 Ordre de Chargement

**Important** : Charger les tables dans cet ordre exact pour faciliter la création des relations :

1. **dim_time.csv** - Table de dimension pour les dates
2. **dim_company.csv** - Table de dimension pour les entreprises
3. **dim_location.csv** - Table de dimension pour les localisation
4. **dim_skills.csv** - Table de dimension pour les compétences
5. **fact_job_offers.csv** - Table de fait principale
6. **fact_job_skills.csv** - Table de fait association

Les tables d'agrégation (agg_*.csv) sont optionnelles - elles peuvent remplacer des agrégations calculées.

### Étape 2 : Transformer les Données (Power Query)

Une fois chargées, vérifier et transformer les données dans Power Query :

1. Cliquez sur **Transformer les données** pour chaque table
2. Pour chaque colonne :
   - Vérifier que le type de données est correct
   - Supprimer les colonnes inutiles
   - Renommer si nécessaire pour la clarté

**Transformations recommandées** :
- Colonnes date : Format `Date`
- Colonnes quantité : Format `Nombre entier`
- Colonnes pourcentage : Format `Nombre décimal`
- Colonnes texte : Format `Texte`

3. Cliquez sur **Fermer et appliquer** une fois les transformations complètes

---

## Configuration du Modèle

### Étape 1 : Créer les Relations

Une fois toutes les données chargées, créer les relations dans l'onglet **Modèle** :

1. Cliquez sur l'onglet **Modèle** (barre supérieure)
2. Cliquez sur **Gérer les relations**
3. Pour chaque relation décrite ci-dessous, cliquez sur **Nouveau**

#### Relations à Créer

| Source | Destination | Type | Cardinalité |
|--------|-------------|------|-------------|
| fact_job_offers[company_id] | dim_company[company_id] | 1-vers-Plusieurs | Beaucoup-vers-Un |
| fact_job_offers[location_id] | dim_location[location_id] | 1-vers-Plusieurs | Beaucoup-vers-Un |
| fact_job_offers[published_date_id] | dim_time[date_id] | 1-vers-Plusieurs | Beaucoup-vers-Un |
| fact_job_skills[job_offer_id] | fact_job_offers[job_offer_id] | 1-vers-Plusieurs | Beaucoup-vers-Un |
| fact_job_skills[skill_id] | dim_skills[skill_id] | 1-vers-Plusieurs | Beaucoup-vers-Un |

### Étape 2 : Marquer les Tables de Rôle

Pour optimiser le modèle :

1. Cliquez sur chaque table de dimension (dim_*)
2. Menu contexte : **Marquer comme table de dimension**
3. Pour chaque table de fait (fact_*) :
   - Menu contexte : **Marquer comme table de fait**

Cela aide Power BI à optimiser les calculs et les recommandations.

---

## Mesures et Calculs DAX

Les mesures sont des calculs personnalisés utilisés dans les visualisations. Créez-les dans la table fact_job_offers.

### Mesures Principales

#### Métriques de Comptage

```dax
-- Total des offres d'emploi
Total Offers = COUNTA(fact_job_offers[job_offer_id])

-- Nombre distinct d'entreprises
Total Companies = DISTINCTCOUNT(fact_job_offers[company_id])

-- Nombre distinct de localisations
Total Locations = DISTINCTCOUNT(fact_job_offers[location_id])

-- Nombre distinct de compétences
Total Skills = DISTINCTCOUNT(fact_job_skills[skill_id])
```

#### Métriques de Pourcentage

```dax
-- Pourcentage de postes en télétravail
Remote % = 
  DIVIDE(
    SUM(fact_job_offers[is_remote]),
    COUNTA(fact_job_offers[job_offer_id]),
    0
  ) * 100

-- Pourcentage de postes permanents
Permanent % =
  DIVIDE(
    SUM(fact_job_offers[is_permanent]),
    COUNTA(fact_job_offers[job_offer_id]),
    0
  ) * 100
```

#### Métriques de Moyenne

```dax
-- Longueur moyenne des descriptions
Avg Description Length = AVERAGE(fact_job_offers[description_length])

-- Nombre moyen de mots
Avg Word Count = AVERAGE(fact_job_offers[word_count])
```

### Mesures par Catégorie d'Emploi

```dax
-- Nombre d'offres Data Engineer
Data Engineer Count = 
  CALCULATE(
    COUNTA(fact_job_offers[job_offer_id]),
    fact_job_offers[job_category] = "Data Engineer"
  )

-- Nombre d'offres Data Scientist
Data Scientist Count =
  CALCULATE(
    COUNTA(fact_job_offers[job_offer_id]),
    fact_job_offers[job_category] = "Data Scientist"
  )

-- Nombre d'offres Data Analyst
Data Analyst Count =
  CALCULATE(
    COUNTA(fact_job_offers[job_offer_id]),
    fact_job_offers[job_category] = "Data Analyst"
  )

-- Nombre d'offres ML Engineer
ML Engineer Count =
  CALCULATE(
    COUNTA(fact_job_offers[job_offer_id]),
    fact_job_offers[job_category] = "ML Engineer"
  )

-- Nombre d'offres Analytics Engineer
Analytics Engineer Count =
  CALCULATE(
    COUNTA(fact_job_offers[job_offer_id]),
    fact_job_offers[job_category] = "Analytics Engineer"
  )
```

### Mesures de Tendance

```dax
-- Croissance année sur année (YoY)
YoY Growth % =
  VAR CurrentYear = YEAR(TODAY())
  VAR PreviousYear = CurrentYear - 1
  RETURN
    DIVIDE(
      CALCULATE([Total Offers], YEAR(fact_job_offers[published_date]) = CurrentYear),
      CALCULATE([Total Offers], YEAR(fact_job_offers[published_date]) = PreviousYear),
      0
    ) - 1

-- Nombre d'offres ce mois-ci
MoM Change =
  VAR CurrentMonth = MONTH(TODAY())
  VAR CurrentYear = YEAR(TODAY())
  RETURN
    CALCULATE(
      [Total Offers],
      MONTH(fact_job_offers[published_date]) = CurrentMonth,
      YEAR(fact_job_offers[published_date]) = CurrentYear
    )
```

---

## Dashboards Recommandés

### Dashboard 1 : Vue d'Ensemble

**Objectif** : Présenter les KPIs principaux et les tendances générales

#### Visualisations

**1. Cartes KPI** (4-6 cartes côte à côte)

```
Colonne 1 : Total Offers (grand nombre)
Colonne 2 : Total Companies
Colonne 3 : Total Locations
Colonne 4 : Total Skills
Colonne 5 : Remote %
Colonne 6 : Permanent %
```

**2. Graphique en Ligne** : Tendance mensuelle des offres

- **Axe X** : dim_time[published_year_month]
- **Axe Y** : [Total Offers]
- **Légende** : fact_job_offers[job_category]
- **Type** : Ligne empilée pour voir les tendances par catégorie

**3. Graphique Circulaire** : Distribution par catégorie

- **Champ** : fact_job_offers[job_category]
- **Valeur** : [Total Offers]
- **Tri** : Descendant par nombre d'offres

**4. Graphique Circulaire** : Distribution par type de contrat

- **Champ** : fact_job_offers[contract_type]
- **Valeur** : [Total Offers]

**5. Graphique Circulaire** : Distribution par type de travail

- **Champ** : fact_job_offers[work_type]
- **Valeur** : [Total Offers]

---

### Dashboard 2 : Analyse par Catégorie d'Emploi

**Objectif** : Explorer en détail les caractéristiques de chaque rôle

#### Visualisations

**1. Tableau Détaillé** : Liste des offres

- **Colonnes** : job_title, company_name, location, contract_type, work_type
- **Filtre interactif** : Sur job_category

**2. Graphique en Barres Empilées** : Types de contrat par catégorie

- **Axe X** : job_category
- **Axe Y** : Comptage des offres
- **Légende** : contract_type
- **Direction** : Horizontal pour meilleure lisibilité

**3. Graphique en Barres Empilées** : Type de travail par catégorie

- **Axe X** : job_category
- **Axe Y** : Comptage
- **Légende** : work_type

**4. Nuage de Points** : Longueur description vs Nombre de mots

- **Axe X** : Longueur moyenne description
- **Axe Y** : Nombre moyen de mots
- **Couleur** : job_category
- **Taille** : Nombre d'offres

---

### Dashboard 3 : Analyse des Compétences

**Objectif** : Identifier les compétences les plus demandées et les tendances

#### Visualisations

**1. Graphique en Barres** : Top 20 compétences

- **Axe X** : dim_skills[skill_name]
- **Axe Y** : COUNT(fact_job_skills[skill_id])
- **Filtre** : Top 20
- **Tri** : Descendant
- **Format** : Horizontal pour lisibilité

**2. Graphique en Barres** : Compétences par catégorie

- **Axe X** : dim_skills[skill_category]
- **Axe Y** : COUNT(fact_job_skills[skill_id])

**3. Graphique en Ligne** : Tendance des 5 meilleures compétences

- **Axe X** : dim_time[published_year_month]
- **Axe Y** : COUNT(fact_job_skills[skill_id])
- **Légende** : Top 5 dim_skills[skill_name]

**4. Matrice** : Skills par catégorie d'emploi

- **Lignes** : job_category
- **Colonnes** : skill_name (Top 10)
- **Valeurs** : COUNT
- **Formatage** : Code couleur intensité

---

### Dashboard 4 : Analyse Géographique

**Objectif** : Comprendre la répartition des offres par lieu

#### Visualisations

**1. Carte** : Offres par pays

- **Localisation** : dim_location[country]
- **Couleur** : [Total Offers]
- **Saturité** : Gradient d'intensité

**2. Carte** : Offres par ville (avec drill-down)

- **Localisation** : dim_location[city]
- **Couleur** : [Total Offers]
- **Interaction** : Permet le zoom sur les régions

**3. Graphique en Barres** : Top 20 villes

- **Axe X** : dim_location[city]
- **Axe Y** : [Total Offers]
- **Tri** : Descendant
- **Format** : Horizontal

**4. Graphique Circulaire** : Télétravail par pays

- **Champ** : dim_location[country]
- **Valeur** : [Remote %]
- **Tri** : Par pourcentage

**5. Tableau** : Métriques de localisation

- **Colonnes** : location, city, country, count_job_offers, count_companies, pct_remote
- **Tri** : Par nombre d'offres

---

### Dashboard 5 : Analyse des Entreprises

**Objectif** : Identifier les entreprises recrutant le plus

#### Visualisations

**1. Graphique en Barres** : Top 20 entreprises

- **Axe X** : dim_company[company_name]
- **Axe Y** : COUNT(fact_job_offers[job_offer_id])
- **Filtre** : Top 20
- **Format** : Horizontal

**2. Tableau** : Détails des entreprises

- **Colonnes** : company_name, location, count_jobs, job_categories, skills_required
- **Tri interactif** : Sur number_of_jobs

**3. Nuage de Bulles** : Analyse des entreprises

- **Axe X** : Nombre d'offres
- **Axe Y** : Nombre moyen de mots dans descriptions
- **Taille** : Nombre d'offres
- **Couleur** : job_category principal

---

### Dashboard 6 : Analytique Avancée

**Objectif** : Analyses statistiques et correlations avancées

#### Visualisations

**1. Histogramme** : Distribution longueur descriptions

- **Champ** : description_length
- **Bins** : 50-100 caractères
- **Type** : Histogramme pour voir la distribution

**2. Jauge KPI** : Score de satisfaction

- **Valeur** : Formule personnalisée basée sur critères
- **Min/Max** : Définir selon vos seuils

**3. Heatmap** : Compétences par localisation

- **Lignes** : dim_location[city]
- **Colonnes** : dim_skills[skill_name]
- **Valeurs** : COUNT
- **Code couleur** : Intensité d'orange à rouge

**4. Heatmap Temporelle** : Offres par jour/heure

- **Lignes** : dim_time[day_name]
- **Colonnes** : Heure (extraite de postedTime)
- **Valeurs** : COUNT
- **Interprétation** : Voir les patterns de publication

---

## Slicers et Filtres

### Slicers à Ajouter

Les slicers permettent aux utilisateurs de filtrer les données interactivement.

#### Slicers Temporels

```
published_year : Dropdown simple (All sélectionné par défaut)
published_month : Dropdown (All)
published_year_month : Timeline (offre la meilleure UX)
```

**Configuration** :
- Ajouter dans la page Overview
- Lier à toutes les visualisations temporelles

#### Slicers de Catégorie

```
job_category : Multi-sélection (toutes coché par défaut)
contract_type : Multi-sélection
work_type : Multi-sélection
```

#### Slicers Géographiques

```
country : Dropdown simple
city : Dropdown (dépendant du pays sélectionné)
```

#### Slicers de Compétences

```
skill_category : Multi-sélection
skill_name : Multi-sélection avec recherche
```

#### Slicers d'Entreprise

```
company_name : Dropdown avec recherche
```

### Configuration des Interactions

Menu : **Format → Interactions**

Pour chaque slicer, configurer :
- Vue d'Ensemble : Filtrer toutes visualisations
- Analyse par Catégorie : Filtrer sur job_category
- Analyse Géographique : Filtrer sur country
- Analyse des Compétences : Filtrer sur skill_category

---

## Mise en Forme

### Palette de Couleurs

Utiliser une palette cohérente pour les catégories d'emploi :

```
Data Engineer       : Bleu (#1f77b4)
Data Scientist      : Orange (#ff7f0e)
Data Analyst        : Vert (#2ca02c)
ML Engineer         : Rouge (#d62728)
Analytics Engineer  : Violet (#9467bd)
Autre               : Gris (#7f7f7f)
```

### Formatage des Champs

```
Nombres entiers     : Format séparateurs (1,000)
Décimales           : 2 décimales maximum
Pourcentages        : Format % avec 1 décimale
Dates               : JJ/MM/AAAA
Descriptions        : Tronquées à 100 caractères max
Noms entreprises    : Sans troncage
```

### Thème et Style

- Utiliser un thème clair pour meilleure lisibilité
- Police : Segoe UI (standard Power BI)
- Taille titre : 14-16 pt
- Taille sous-titre : 11-12 pt
- Taille légende : 10 pt

---

## Optimisation des Performances

### Bonnes Pratiques

1. **Utiliser des agrégations** pour les grandes tables
   - Pré-calculer les sommes/moyennes
   - Réduire le nombre de lignes interrogées

2. **Ajouter des filtres implicites**
   - Filtrer par année par défaut
   - Réduire la portée des données initiales

3. **Optimiser le modèle de données**
   - Supprimer les colonnes inutiles
   - Créer des relations explicites
   - Marquer dimensions et faits correctement

4. **Utiliser le mode d'import vs DirectQuery**
   - Import : Plus rapide, consomme plus de mémoire
   - DirectQuery : Moins de mémoire, requêtes plus lentes
   - Recommandation : Import pour ce volume

5. **Tester les performances régulièrement**
   - Menu Affichage : Performance Analyzer
   - Identifier les visualisations lentes
   - Optimiser les mesures DAX lentes

### Requête de Test Performance

```dax
-- Vérifier la performance des agrégations
EVALUATE
SUMMARIZECOLUMNS(
    fact_job_offers[job_category],
    dim_time[published_year_month],
    "Total Offers", COUNTA(fact_job_offers[job_offer_id]),
    "Avg Description", AVERAGE(fact_job_offers[description_length]),
    "Remote %", [Remote %]
)
```

---

## Publication et Partage

### Publier sur Power BI Service

1. Menu : **Fichier → Publier**
2. Sélectionner l'espace de travail Power BI
3. Configurer les paramètres de publication
4. Cliquer sur **Sélectionner**

**Note** : Nécessite un compte Power BI (gratuit ou Pro)

### Configuration du Rafraîchissement Automatique

Pour que les données se mettent à jour automatiquement :

1. Accéder au **Power BI Service** en ligne
2. Accéder au dataset
3. Menu : **Paramètres → Actualisation programmée**
4. Configurer :
   - **Plage horaire** : 02:00 - 06:00 UTC (évite heures peak)
   - **Fréquence** : Quotidienne
   - **Notifier** : En cas d'erreur

### Partage avec l'Équipe

1. Dans Power BI Service
2. Cliquer sur **Partager**
3. Inviter les utilisateurs ou groupes
4. Définir les permissions (lecture, modification)

---

## Dépannage

### Données Manquantes

**Symptômes** : Les chiffres ne correspondent pas ou certaines données manquent

**Solutions** :
- Vérifier les relations ont été créées correctement
- Vérifier la cardinalité des relations
- Consulter Performance Analyzer (Affichage → Performance Analyzer)
- Valider les données source dans les fichiers CSV

### Performances Lentes

**Symptômes** : Les dashboards chargent lentement, les filtres sont lents

**Solutions** :
- Réduire la plage temporelle par défaut
- Ajouter des agrégations pré-calculées
- Vérifier que le mode Import est utilisé
- Réduire les visualisations par page
- Optimiser les mesures DAX complexes

### Calculs Incorrects

**Symptômes** : Les valeurs affichées ne sont pas correctes

**Solutions** :
- Vérifier les mesures DAX
- Vérifier le contexte de filtre appliqué
- Tester avec des valeurs simples manuellement
- Vérifier les formules CALCULATE() ont un filtre approprié

### Erreurs de Chargement de Données

**Symptômes** : "Erreur lors du chargement des données"

**Solutions** :
- Vérifier le chemin vers les fichiers CSV
- Vérifier les fichiers existent et ne sont pas corrompus
- Vérifier les droits de lecture
- Réessayer le chargement

---

## Résumé des KPIs Clés

| KPI | Mesure | Objectif | Fréquence |
|-----|--------|----------|-----------|
| Total Offers | COUNTA() | Monitoring | Quotidien |
| Growth MoM | Changement % | +5% | Mensuel |
| Companies | DISTINCTCOUNT() | 3000+ | Trimestriel |
| Skills Diversity | DISTINCTCOUNT() | 25+ | Trimestriel |
| Remote % | SUM/COUNT | 30%+ | Quotidien |
| Permanent % | SUM/COUNT | 70%+ | Quotidien |

---

## Informations Document

- **Créé** : Janvier 2026
- **Version** : 1.0
- **Pour** : Projet JOB INTELLIGENT
- **Dernière mise à jour** : Janvier 2026

---

**Pour toute question sur la configuration ou les dashboards, consulter la documentation du projet ou les logs d'exécution DBT.**
