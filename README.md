# Pershop-pilote
Copilote intelligent pour le matching **client ↔ personal shopper** et la préparation de séance.

## 1. Présentation du projet

Pershop Pilote est un prototype d’application web permettant :

### Côté Client :
- de remplir un formulaire simple et intuitif,  
- d’être analysé automatiquement par un algorithme de matching,  
- de recevoir une liste de personal shoppers qui correspondent réellement à son style, son budget, sa ville, son objectif et ses besoins personnels,  
- d’obtenir une explication IA personnalisée (via Groq) sur le meilleur profil recommandé.

### Côté Personal Shopper :
- d’accéder à son espace dédié,  
- de voir uniquement les clients qui lui ont été assignés,  
- d’obtenir un **pré-brief IA complet**, structuré et professionnel pour préparer la séance.

## 2. Fonctionnalités principales

### Matching automatisé  
Un algorithme évalue la compatibilité client → shopper selon :
- ville / géolocalisation (présentiel, visio, peu importe),  
- styles vestimentaires souhaités,  
- budget réel,  
- objectifs (exemple : mariage, confiance en soi, relooking pro…),  
- moments de vie,  
- morphologie et préférences,  
- tags et spécialités du personal shopper.

### Intelligence artificielle (Groq)  
L’IA génère :
- un texte d’explication clair pour le client,
- un pré-brief structuré pour le personal shopper.

Modèle utilisé :  
```
llama-3.3-70b-versatile
```

### Gestion des deux interfaces  
- **Client** : formulaire + recommandations + analyse IA  
- **Personal Shopper** : liste des clients assignés + pré-brief

### Persistance légère  
Les clients sont stockés en CSV via écriture append.

---

## 3. Technologies utilisées

### Frontend
- **Streamlit**

### Backend
- **Python**
- **Groq SDK**
- **Matching basé sur règles métier + IA**

### Stockage
- CSV local (`clients.csv`)
- JSON inline pour les shoppers

---

## 4. Installation

### 1. Cloner le projet
```bash
git clone https://github.com/ton-projet/pershop-pilote.git
cd pershop-pilote
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configurer la clé API Groq
Créer un fichier `.env` :
```
GROQ_API_KEY=ta_cle_api
```

### 4. Lancer l'application
```bash
streamlit run app.py
```

---

## 5. Structure du projet
```
pershop-pilote/
│
├── app.py
├── shoppers.py
├── matching.py
├── clients.csv
├── .env
├── README.md
└── requirements.txt
```

---

## 6. Améliorations prévues
- Ajout d’images pour les personal shoppers  
- Tableau de bord avancé pour shoppers  
- Matching hybride règles + embeddings  
- Backend FastAPI  
- Authentification  
- Passage à PostgreSQL/Supabase

---

## 7. Objectif du prototype
Prototype démonstratif du potentiel d’un agent IA appliqué au personal shopping.