# Simulateur de capteurs IoT (MQTT)

Ce projet simule trois capteurs (température, humidité, GPS), publie leurs mesures en JSON vers un broker MQTT (ex: Mosquitto) et propose un **dashboard web** (Flask) pour visualiser les données en temps réel.

## 👤 Auteur
**Nom : Ghaith Riabi**

## 🚀 Prérequis
- Python 3.9+ (Windows/Linux)
- `pip` et (optionnel) `virtualenv`
- Broker MQTT (ex: **Eclipse Mosquitto**) qui écoute sur `localhost:1883`

## 🧩 Installation (Windows)
```powershell
# 1) Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate

# 2) Installer les dépendances
pip install -r requirements.txt
```

> **Mosquitto**: installez Eclipse Mosquitto, puis démarrez le service. Par défaut, il écoute sur le port **1883**.

## ▶️ Lancer le simulateur
```powershell
python main.py --host localhost --port 1883 --interval 1 --qos 0 --temp-center 22
```
Les messages sont publiés sur:
- `iot/sensor/temperature`
- `iot/sensor/humidity`
- `iot/sensor/gps`

## 📊 Lancer le dashboard
Dans un autre terminal (toujours activé):
```powershell
python dashboard/app.py
```
Puis ouvrez http://localhost:5000

## 🛠️ Arrêt propre
Appuyez sur `Ctrl+C` dans le terminal du simulateur. Le client MQTT s'arrête proprement.

## 🧪 Exemple de payload JSON
```json
{
  "timestamp": "2025-11-23T15:00:00+00:00",
  "sensor": "temperature",
  "value": 22.4,
  "unit": "C"
}
```

## 📁 Structure réelle du projet
```
project-root/
├─ architecture.png          # Diagramme d'architecture
├─ data.json                 # Historique des mesures en JSON
├─ main.py                   # Code principal (simulateur)
├─ main_oldversion.py        # Ancienne version du simulateur
├─ mqtt_client.py            # Client MQTT (publication JSON)
├─ sensors.py                # Classes des capteurs
├─ rapport.docx              # Rapport détaillé (5 pages)
├─ README.md                 # Documentation
├─ dashboard/                # Application Flask (UI + MQTT subscriber)
│  ├─ app.py
│  ├─ templates/index.html
│  └─ static/{app.js, style.css}
├─ utils/                    # Configurations et utilitaires
├─ venv/                     # Environnement virtuel Python
└─ __pycache__/              # Fichiers compilés Python
```

## 🔒 Notes QoS
QoS=0 par défaut (au moins une fois). Vous pouvez passer `--qos 1` pour une livraison **au moins une fois** (ack PUBLISH/PUBACK), ou `--qos 2` pour **exactement une fois** (plus coûteux).
