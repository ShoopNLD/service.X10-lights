# X10 - Lights (Domotica Commander)

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](LICENSE)
[![XBMC / Kodi](https://img.shields.io/badge/Kodi-v12%20--%20v21%2B-blue)](https://kodi.tv/)
[![Version](https://img.shields.io/badge/Version-v2.0.0-green)](https://github.com/ShoopNLD/service.X10-lights)

🌐 **Taal / Language:** **Nederlands 🇳🇱** | [English 🇬🇧](README.md)

---

**X10 - Lights (Domotica Commander)** (`service.X10-lights`) is een achtergrondservice add-on voor XBMC / Kodi die bioscoopverlichting en domotica-apparaten automatisch bedient op basis van mediaspeler- en systeemgebeurtenissen.

![XBMC Picture](docs/screenshots/XBMC%20picture.png)

---

## 📖 Geschiedenis & Context
Het project is tussen **2011 en 2014** ontwikkeld door **Majestic Soft** voor een dedicated thuisbioscoop en destijds breed gedeeld op het officiële XBMC/Kodi-forum. 

Het doel was simpel doch magisch: de ultieme bioscoopervaring creëren in de huiskamer:
- Zodra een film start, dimmen de lichten geleidelijk;
- Bij een pauze gaan ze zachtjes aan op sfeersterkte voor een drankje of toiletbezoek;
- Zodra de film stopt of afloopt, gaan de lichten weer helder branden.

Deze repository bewaart zowel de **complete historische tijdlijn (2011–2014)** van V0.0.1 t/m V1.0.4, als de gemoderniseerde **V2.0.0 release** voor moderne Kodi-versies (Python 3).

---

## ⚡ Belangrijkste Functies

- **Automatische Event Triggers:**
  - `X_Start` – Kodi/XBMC opstarten (bijv. sfeerverlichting inschakelen)
  - `X_Stop` – Kodi/XBMC afsluiten (bijv. alle filmverlichting uit)
  - `P_Start` – Starten van video playback (lichten dimmen / uit)
  - `P_Pause` – Pauzeren van video playback (sfeerstand / oriëntatielicht)
  - `P_Resume` – Hervatten van playback (lichten direct weer dimmen)
  - `P_Stop` – Handmatig stoppen van video (verlichting aan)
  - `P_End` – Einde van video bereikt (verlichting rustig aan)
- **Multi-Device ondersteuning:** Onafhankelijke aansturing van tot maximaal **5 apparaten of groepen**.
- **Acties per event:** Keuze uit `ON`, `OFF`, `DIM`, `BRIGHT` (0–100%) of aangepaste *Vrije Commando's* (Free Commands).
- **Tweetalige interface:** Volledig instelbaar in het **Nederlands** en **Engels**.
- **Ingebouwde diagnostiek:** Uitgebreide debug-logging optie voor traceerbaarheid.

---

## 🔌 Ondersteunde Domoticasystemen

| Domoticasysteem | Protocol / Methode | Beschrijving |
| :--- | :--- | :--- |
| **X10-Commander** | HTTP / API | Melloware X10-Commander apparaat commando's |
| **HomeSeer** | HTTP POST REST | Directe HomeSeer apparaat-aansturing |
| **tenHsServer** | HTTP GET | HomeSeer koppeling via tenHsServer extensie |
| **Switch King** | HTTP REST | REST API calls naar Switch King server |
| **Thinking Home** | HTTP GET | Thinking Home webserver interface |
| **HomeWizard** | HTTP REST | Lokale HomeWizard HTTP API |
| **Domoticz** | HTTP JSON API | Domoticz schakelen en dimmen (level 0–16) |
| **HomeGenie** | HTTP REST | HomeGenie API (bijdrage door Mack) |
| **LightWaveRF** | UDP Broadcast | Directe UDP socket communicatie naar LightWaveRF WiFi Link |

---

## 🚀 Wat is er nieuw in V2.0.0 (Python 3 Migratie)

- **Python 3 Compatibiliteit:** Volledig gemigreerd voor Kodi 19 Matrix, Kodi 20 Nexus, Kodi 21 Omega en Kodi 22 Piers+.
- **Event-driven Monitor:** De verouderde polling loop met `xbmc.sleep(1000)` is vervangen door `xbmc.Monitor().waitForAbort()`. Sluit direct af bij het stoppen van Kodi zonder CPU-overhead.
- **Non-blocking I/O & Timeouts:** Netwerk-aanroepen via `urllib.request` met expliciete 5-seconden timeouts, zodat Kodi nooit bevriest bij netwerkstoringen.
- **UDP Bytes Encoding:** Veilige socket payload encoding (`utf-8`) voor LightWaveRF.
- **Officiële PO Vertalingen:** Tweetalige catalogi in gettext formaat (`resource.language.nl_nl` en `resource.language.en_gb`).

---

## 📂 Repository Structuur

```text
Proj_X10-Lights/
├── .gitignore               # Negeert python caches, OS bestanden en packages
├── LICENSE                  # GNU General Public License v2
├── README.md                # Internationale Engelse documentatie
├── README.nl.md             # Nederlandse documentatie (dit bestand)
├── CHANGELOG.md             # Volledige release-historie (v0.0.1 t/m v2.0.0)
├── docs/
│   ├── Manual - XBMC service.X10-lights (uk) R1.0.4.pdf   # Originele 18-pagina handleiding
│   └── screenshots/         # Schermafbeeldingen van instellingen en interface
└── service.X10-lights/      # De officiële Kodi Add-on map
    ├── addon.xml            # Add-on metadata en service entry-points
    ├── default.py           # Python 3 service logica
    ├── changelog.txt        # Add-on changelog
    ├── icon.png             # Add-on icoon
    └── resources/
        ├── settings.xml     # Instellingen configuratiemenu
        └── language/        # Taalbestanden (.po en .xml)
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

## 🛣️ Toekomstige Uitbreidingen (Roadmap)
- [ ] **Home Assistant:** Integratie via Webhooks en REST API voor directe integratie met moderne slimme lampen (Philips Hue, Zigbee, Z-Wave).
- [ ] **MQTT:** Publiceren van Kodi events naar een MQTT broker voor universele automatisering.
- [ ] **Asynchrone Event Queue:** Volledige threading/async event-afhandeling.

---

## 📄 Licentie
Dit project is gelicentieerd onder de **GNU General Public License (GPL v2)** - zie het bestand [LICENSE](LICENSE) voor details.

**Auteur:** Majestic Soft  
**E-mail:** X10-Lights@majesticsoft.nl  
**Forum:** [Kodi Community Forum Topic](https://forum.kodi.tv/)
