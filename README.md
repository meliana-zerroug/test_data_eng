# 🎮 Steam Games Data Engineering Project

Projet de scraping et visualisation des données Steam avec MongoDB et Streamlit.

##  Prérequis

- **Docker Desktop** installé et lancé ([Télécharger ici](https://www.docker.com/products/docker-desktop))

## Installation et lancement

###  Lancer l'application (une seule commande !)

```bash
docker-compose up -d --build
```

**Explication** : Cette commande :
- Télécharge les images Docker (Python, MongoDB)
- Construit l'application Streamlit
- Lance les 2 conteneurs (MongoDB + Streamlit)
- Charge automatiquement les données CSV dans MongoDB
- Mode `-d` = détaché (tourne en arrière-plan)

**Note** : Les données sont chargées automatiquement au démarrage depuis `steam_project/data/steam_search.csv`.

###  Accéder à l'application

**En local** : Ouvrez votre navigateur sur **http://localhost:8501**

**Sur GitHub Codespaces** : VS Code ouvrira automatiquement un lien du type :
- `https://[votre-codespace]-8501.app.github.dev/`
- Ou cliquez sur l'onglet "Ports" en bas et ouvrez le port 8501

---

## Fonctionnalités


---

##  Commandes utiles

### Voir les logs en temps réel

```bash
docker-compose logs -f streamlit
```

### Arrêter l'application

```bash
docker-compose down
```

### Relancer l'application

```bash
docker-compose down
docker-compose up -d --build
```

### Accéder à MongoDB directement

```bash
docker exec -it steam_mongodb mongosh
# Puis dans MongoDB shell :
use projet
db.steam_games.find().limit(5)
```


---

##  Fonctionnement

```
1. Scrapy Spider → Scrape Steam → steam_search.csv
2. Docker Compose démarre MongoDB + Streamlit
3. start.sh → Charge automatiquement CSV → MongoDB
4. app.py (Streamlit) → Lit MongoDB → Affiche dans le navigateur
```

---

##  Choix techniques


---

## Résolution de problèmes

### L'application ne démarre pas

```bash
# Vérifier que Docker est bien lancé
docker --version

# Vérifier les conteneurs actifs
docker ps
```

### Les données ne s'affichent pas (Total de jeux = 0)

Les données sont normalement chargées automatiquement au démarrage. Si elles ne s'affichent pas :

```bash
# Reconstruire et relancer les conteneurs
docker-compose down
docker-compose up -d --build

# Attendre 10 secondes que MongoDB se lance et que les données soient chargées
# Puis vérifier les logs
docker logs steam_app
```

### MongoDB ne se connecte pas

```bash
# Redémarrer les conteneurs
docker-compose down
docker-compose up -d --build
```

### Port 8501 déjà utilisé

```bash

# Arrêter le conteneur existant
docker-compose down

# Ou changer le port dans docker-compose.yml
ports:
  - "8502:8501"  # Utiliser le port 8502 au lieu de 8501
```

---


### Ports utilisés

- **8501** : Application Streamlit
- **27017** : MongoDB



---




