# X10 - Lights (Domotica Commander)

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](LICENSE)
[![XBMC / Kodi](https://img.shields.io/badge/Kodi-v12%20--%20v21%2B-blue)](https://kodi.tv/)
[![Release](https://img.shields.io/badge/Release-v1.0.4-green)](https://github.com/)

**X10 - Lights (Domotica Commander)** (`service.X10-lights`) is een achtergrondservice add-on voor XBMC / Kodi die bioscoopverlichting en domotica-apparaten automatisch bedient op basis van mediaspeler- en systeemgebeurtenissen.

![XBMC Picture](docs/screenshots/XBMC%20picture.JPG)

---

## 📖 Geschiedenis & Context
Het project is tussen **2011 en 2014** ontwikkeld door **Majestic Soft** voor een dedicated thuisbioscoop en destijds breed gedeeld op het officiële XBMC/Kodi-forum. 

Het doel was simpel doch magisch: de ultieme bioscoopervaring creëren. Zodra een film begint dimmen de lichten geleidelijk; bij pauzeren gaan ze op sfeersterkte aan; en zodra de film stopt of afloopt gaan de lichten weer helder branden.

Deze repository bewaart zowel het **volledige historische archief (2011–2014)** van V0.0.1 t/m V1.0.4, als de basis voor de moderne doorontwikkeling (Python 3 en Kodi 20/21/22+).

---

## ⚡ Belangrijkste Functies (V1.0.4)

- **Automatische Event triggers:**
  - `X_Start` – Kodi/XBMC opstarten
  - `X_Stop` – Kodi/XBMC afsluiten
  - `P_Start` – Starten van video playback (lichten dimmen / uit)
  - `P_Pause` – Pauzeren van video playback (oriëntatieverlichting / sfeerstand)
  - `P_Resume` – Hervatten van playback (lichten weer dimmen)
  - `P_Stop` – Handmatig stoppen van video (verlichting aan)
  - `P_End` – Einde van film/aflevering bereikt (verlichting aan)
- **Multi-Device ondersteuning:** Onafhankelijke aansturing van tot maximaal **5 apparaten/lampen**.
- **Acties per event:** Keuze uit `ON`, `OFF`, `DIM`, `BRIGHT` (0–100%) of aangepaste *Free Commands*.
- **Tweetalige interface:** Volledig instelbaar in het **Nederlands** en **Engels**.
- **Ingebouwde diagnostiek:** Uitgebreide debug-logging optie voor probleemoplossing.

---

## 🔌 Ondersteunde Domoticasystemen

In versie 1.0.4 worden de volgende systemen en protocollen ondersteund:

| Domoticasysteem | Protocol / Methode | Beschrijving |
| :--- | :--- | :--- |
| **X10-Commander** | UDP / HTTP | Melloware X10-Commander API calls |
| **HomeSeer** | HTTP REST | Directe HomeSeer apparaat-aansturing |
| **tenHsServer** | HTTP | HomeSeer koppeling via tenHsServer |
| **Switch King** | HTTP REST | REST API calls naar Switch King server |
| **Thinking Home** | HTTP | Thinking Home webserver interface |
| **HomeWizard** | HTTP REST | Lokale HomeWizard HTTP API |
| **Domoticz** | HTTP JSON API | Domoticz schakelen en dimmen |
| **HomeGenie** | HTTP REST | HomeGenie API (bijdrage door Mack) |
| **LightWaveRF** | UDP Broadcast | Directe UDP socket broadcasts naar LightWaveRF WiFi Link |

---

## 📂 Repository Structuur

```text
Proj_X10-Lights/
├── .gitignore               # Negeert python caches, OS bestanden en packages
├── LICENSE                  # GNU General Public License v2
├── README.md                # Dit projectoverzicht
├── CHANGELOG.md             # Volledige release-historie (v0.0.1 t/m v1.0.4)
├── docs/
│   ├── Manual - XBMC service.X10-lights (uk) R1.0.4.pdf   # Originele 18-pagina handleiding
│   └── screenshots/         # Schermafbeeldingen van instellingen en interface
└── service.X10-lights/      # De officiële Kodi Add-on map
    ├── addon.xml            # Add-on metadata en service entry-points
    ├── default.py           # Python service logica
    ├── changelog.txt        # Add-on changelog
    ├── icon.png             # Add-on icoon
    └── resources/
        ├── settings.xml     # Instellingen configuratiemenu
        └── language/        # Taalbestanden (Dutch & English strings.xml)
```

---

## 📸 Schermafbeeldingen

| Add-on Categorieën | Apparaat Instellingen |
| :---: | :---: |
| ![Settings 01](docs/screenshots/screenshot%2001.JPG) | ![Settings 02](docs/screenshots/screenshot%2002.JPG) |

| Event Configuratie | Vrije Commando's |
| :---: | :---: |
| ![Settings 03](docs/screenshots/screenshot%2003.JPG) | ![Settings 04](docs/screenshots/screenshot%2004.JPG) |

---

## 📚 Documentatie
De originele, uitgebreide handleiding is als PDF te vinden in de `docs/` map:
- 📄 [Manual - XBMC service.X10-lights (uk) R1.0.4.pdf](docs/Manual%20-%20XBMC%20service.X10-lights%20(uk)%20R1.0.4.pdf)

---

## 🚀 Roadmap & Modernisatie (v2.0.0+)

Voor moderne versies van Kodi (Nexus v20, Omega v21, Piers v22+) wordt het project gemoderniseerd:
1. **Python 3 Migratie:**
   - Vervangen van `urllib` / `urllib2` door `urllib.request` / `urllib.parse`.
   - Veilige UDP socket encoding (`bytes`/`utf-8`) voor LightWaveRF.
   - Ombouw van `xbmc.abortRequested` polling naar event-driven `xbmc.Monitor().waitForAbort()`.
   - Update `addon.xml` naar `xbmc.python` versie `3.0.0+`.
2. **Moderne Domotica Integraties:**
   - **Home Assistant:** Ondersteuning voor REST API en webhooks voor directe integratie met moderne slimme verlichting (Hue, Zigbee, Z-Wave).
   - **MQTT:** Directe publishing naar een MQTT-broker voor universele domotica-aansturing.
3. **Refactor & Schaalbaarheid:**
   - Objectgeoriënteerde Device-architectuur.
   - Asynchrone / non-blocking netwerk-aanroepen om Kodi playback nooit te blokkeren.

---

## 📄 Licentie
Dit project is gelicentieerd onder de **GNU General Public License (GPL)** - zie het bestand [LICENSE](LICENSE) voor details.

**Auteur:** Majestic Soft  
**Contact:** X10-Lights@majesticsoft.nl
