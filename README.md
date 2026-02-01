# 🎮 Steam Games Data Engineering Project

Projet de scraping et visualisation des données Steam avec MongoDB et Streamlit.

##  Prérequis

- **Docker Desktop** installé et lancé ([Télécharger ici](https://www.docker.com/products/docker-desktop))

## Installation et lancement

###  Lancer l'application avec Docker Compose

```bash
docker-compose up -d
```

**Explication** : Cette commande :
- Télécharge les images Docker (Python, MongoDB)
- Construit l'application Streamlit
- Lance les 2 conteneurs (MongoDB + Streamlit)
- Mode `-d` = détaché (tourne en arrière-plan)

###  Charger les données dans MongoDB

```bash
docker exec steam_app python steam_mongoDB.py
```

**Note** : Les données du fichier `steam_project/data/steam_search.csv` sont déjà présentes dans le projet.

###  Accéder à l'application

Ouvrez votre navigateur : **http://localhost:8501**

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
docker-compose up -d
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
2. steam_mongoDB.py → Charge CSV → MongoDB
3. app.py (Streamlit) → Lit MongoDB → Affiche dans le navigateur
4. Docker Compose → Orchestre MongoDB + Streamlit
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

# Voir les logs d'erreur
docker-compose logs
```

### MongoDB ne se connecte pas

```bash
# Redémarrer les conteneurs
docker-compose down
docker-compose up -d

# Attendre un peu et recharger les données
docker exec steam_app python steam_mongoDB.py
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




