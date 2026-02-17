# Projet Cloud & DevOps – Plateforme de diffusion de contenu cloud-native

Ce dépôt contient l’implémentation d’une plateforme de diffusion de contenu développée dans le cadre du TP de Cloud Computing. L’application permet de lire des données stockées dans Azure Blob Storage, de les exposer via une API REST et de les visualiser à travers une interface web minimale. Le projet est conteneurisé avec Docker, déployable sur Kubernetes (AKS) et automatisé via une pipeline CI/CD GitHub Actions.

Un seul README est nécessaire pour le projet. Le second README éventuellement présent dans le dépôt correspondait uniquement à une explication interne du frontend intégré et peut être supprimé afin d’éviter toute confusion.

Structure du projet :

backend/ → application Flask, API et interface web  
backend/app/ → code principal de l’application  
backend/tests/ → tests automatisés  
backend/k8s/ → fichiers de déploiement Kubernetes  
backend/requirements.txt → dépendances Python  
backend/wsgi.py → point d’entrée serveur  
Dockerfile → construction de l’image Docker  
README.md → documentation du projet  

L’application Flask fournit les endpoints requis :
/api/events  
/api/news  
/api/faq  
/healthz  
/readyz  

Un cache mémoire TTL est utilisé afin de réduire les accès répétés au stockage.

L’interface web demandée par le TP est intégrée directement dans Flask via les dossiers backend/app/templates et backend/app/static. Aucun frontend séparé n’est requis.

Exécution locale :

cd backend  
python -m venv .venv  
source .venv/bin/activate    (Linux/Mac)  
.\.venv\Scripts\Activate.ps1 (Windows PowerShell)  
pip install -r requirements.txt  

Configurer ensuite les variables d’environnement nécessaires, puis lancer :

python -m app

L’application devient accessible via :
Interface web : http://localhost:8080  
API : http://localhost:8080/api/events  
Santé : http://localhost:8080/healthz et /readyz  

Tests automatisés :

pytest backend/tests

Les tests ne nécessitent pas de connexion réelle à Azure.

Exécution via Docker :

docker build -t content-api:local .  
docker run --rm -p 8080:8080 -e AZURE_STORAGE_CONNECTION_STRING="..." content-api:local  

Déploiement Kubernetes :

Les fichiers de déploiement se trouvent dans backend/k8s/.

Avant déploiement :
- renseigner la connexion Azure dans secret.yaml
- vérifier l’image utilisée dans deployment.yaml

Déploiement :
kubectl apply -k backend/k8s

Pipeline CI/CD :

La pipeline GitHub Actions automatise les tests, la construction de l’image Docker, la publication vers GHCR, le déploiement sur AKS et un test de fonctionnement après déploiement.

Secrets nécessaires dans GitHub :
AZURE_CREDENTIALS  
AKS_RESOURCE_GROUP  
AKS_CLUSTER_NAME  

Conformité au sujet :

Le projet respecte les contraintes demandées : lecture des données depuis Azure Blob Storage, endpoints API imposés, cache mémoire TTL, tests automatisés, conteneur Docker optimisé, déploiement Kubernetes complet et pipeline CI/CD fonctionnelle.

Remarque finale :

L’architecture reste volontairement simple afin de faciliter l’exécution et la maintenance tout en respectant les exigences pédagogiques, tout en permettant une évolution future vers une architecture plus complète si nécessaire.

# Plateforme-de-diffusion-de-contenu-statique-cloud-native
Gemini said Concevez une plateforme cloud-native sur AKS pour diffuser du contenu (JSON/YAML) via une API Flask. Stockée sur Azure Blob Storage, la solution doit être automatisée par GitHub Actions, scalable et sécurisée. Livrables : architecture, conteneurisation Docker, monitoring et rapport de justification.
