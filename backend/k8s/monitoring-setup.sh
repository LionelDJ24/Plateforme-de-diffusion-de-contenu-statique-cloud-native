# Azure Monitor – Configuration basique
# À exécuter via Azure CLI après déploiement AKS
# Prérequis : az login, extension monitor installée

# --- Variables ---
RESOURCE_GROUP="<votre-resource-group>"
AKS_CLUSTER="<votre-cluster-aks>"
LOCATION="francecentral"
ACTION_GROUP_EMAIL="<votre-email>"

# 1. Activer les métriques Container Insights sur AKS
az aks enable-addons \
  --resource-group $RESOURCE_GROUP \
  --name $AKS_CLUSTER \
  --addons monitoring

# 2. Créer un Action Group (destinataire des alertes)
az monitor action-group create \
  --resource-group $RESOURCE_GROUP \
  --name "content-platform-alerts" \
  --short-name "cp-alerts" \
  --action email admin $ACTION_GROUP_EMAIL

# 3. Alerte CPU élevé (>80% pendant 5 minutes)
az monitor metrics alert create \
  --name "alert-cpu-high" \
  --resource-group $RESOURCE_GROUP \
  --scopes $(az aks show -g $RESOURCE_GROUP -n $AKS_CLUSTER --query id -o tsv) \
  --condition "avg cpu_usage_percentage > 80" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action "content-platform-alerts" \
  --description "CPU AKS supérieur à 80%"

# 4. Alerte mémoire élevée (>85% pendant 5 minutes)
az monitor metrics alert create \
  --name "alert-memory-high" \
  --resource-group $RESOURCE_GROUP \
  --scopes $(az aks show -g $RESOURCE_GROUP -n $AKS_CLUSTER --query id -o tsv) \
  --condition "avg memory_usage_percentage > 85" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action "content-platform-alerts" \
  --description "Mémoire AKS supérieure à 85%"

# 5. Alerte erreurs HTTP 5xx via Log Analytics (Container Insights)
# Requête KQL – à créer manuellement dans Azure Monitor > Alertes > Créer
# Coller cette requête dans une alerte de type "Log search" :
#
# ContainerLog
# | where LogEntry contains "HTTP/1." and LogEntry contains " 5"
# | where TimeGenerated > ago(5m)
# | summarize count() by bin(TimeGenerated, 1m)
# | where count_ > 5
#
# Seuil : count > 5 erreurs 5xx en 1 minute
# Fréquence d'évaluation : 1 minute
# Fenêtre : 5 minutes
# Sévérité : 2 (Warning)
