# 📉 Projet : Simulation du Système de Retraite (Maroc)

Ce projet consiste en une simulation discrète visant à étudier la viabilité du système de retraite et à anticiper une crise potentielle. L'étude se concentre sur l'impact du prolongement de l'âge de départ à la retraite de **63 à 65 ans** ainsi que sur d'autres réformes paramétriques.

---

## 📝 Contexte & Objectifs

La simulation modélise l'évolution d'une caisse de retraite fictive (inspirée de la fonction publique marocaine) sur une période de **11 années** (2025 - 2035).

* **Population initiale** : 10 000 employés actifs et 1 000 retraités.
* **Réserve initiale** : 200 Millions de Dirhams (Mdhs).
* **Objectif** : Éviter l'effondrement de la réserve via différents scénarios de réforme.

---

## 📊 Scénarios Simulés

L'application compare 4 scénarios distincts pour évaluer leur efficacité:

| Scénario | Âge Retraite | Cotisations | Pension (Formule) |
| :--- | :---: | :---: | :--- |
| **1. Actuel** | 63 ans | Taux actuels | `(NAT * 2%) * DSAR` |
| **2. Extension** | **65 ans** | Taux actuels | `(NAT * 2%) * DSAR` |
| **3. Extension + Cotis.** | 65 ans | **Augmentés** | `(NAT * 2%) * DSAR` |
| **4. Mixte** | 65 ans | Augmentés | **`(NAT * 1.5%) * DSAR`** |

> **Légende** :
> * *NAT* : Nombre d'Années Travaillées
> * *DSAR* : Dernier Salaire Avant Retraite

---

## 📈 Indicateurs Clés de Performance (KPI)

Pour chaque année simulée (fin décembre), les indicateurs suivants sont mesurés:

1.  **TotEmp** : Nombre total d'employés actifs.
2.  **TotRet** : Nombre total de retraités.
3.  **TotCotis** : Montant total des cotisations collectées.
4.  **TotPens** : Montant total des pensions versées.
5.  **Reserve** : État de la réserve de la caisse.
6.  **NouvRet** : Nombre de nouveaux départs en retraite.
7.  **NouvRec** : Nombre de nouveaux recrutements.

---

## ⚙️ Paramètres du Modèle

Le modèle mathématique intègre les distributions suivantes:

* **Salaires & Âges** : Distributions probabilistes définies (voir rapport).
* **Recrutement** : Entre 250 et 400 nouveaux employés/an (Loi Uniforme).
* **Avancement** : Augmentation de salaire de **5% tous les 5 ans** (2025, 2030, 2035).
* **Cotisations** : Taux progressifs selon la tranche de salaire (5% à 10% pour les scénarios 1 & 2).

---

## 🚀 Installation et Configuration

### Prérequis

* **Python** (v3.8+ recommandé)
* **pip** (Gestionnaire de paquets Python)

### 1. Installation

> [!TIP]
> Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet.

1.  **Cloner ou télécharger le projet** dans votre dossier de travail.
      ```bash
    git clone https://github.com/somi2306/GestionConges.git
    ```
2.  **Créer un environnement virtuel** (Optionnel) :
    ```bash
    python -m venv venv
    # Activer sur Windows
    venv\Scripts\activate
    # Activer sur Mac/Linux
    source venv/bin/activate
    ```
3.  **Lancer le programme principal**  :
    ```bash
    python main.py
    ```

> [!TIP]
> Le programme permet de configurer les **germes (seeds)** des générateurs aléatoires pour assurer la reproductibilité des résultats entre les scénarios.

---

## 📂 Structure des Résultats

Les résultats sont générés sous deux formes:

1.  **Tableaux** :
    * États annuels des indicateurs pour une simulation donnée.
    * Moyennes sur **40 simulations** (Monte Carlo) pour les années 2025, 2030, 2035.
    * Intervalles de confiance à 95% pour la *Reserve*.
2.  **Graphiques** :
    * Évolution de la réserve (Comparaison des 4 scénarios).
    * Démographie (Actifs vs Retraités).
