# X10 - Lights (Domotica Commander)

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](LICENSE)
[![XBMC / Kodi](https://img.shields.io/badge/Kodi-v12%20--%20v21%2B-blue)](https://kodi.tv/)
[![Version](https://img.shields.io/badge/Version-v2.0.0-green)](https://github.com/ShoopNLD/service.X10-lights)

🌐 **Language / Taal:** **English 🇬🇧** | [Nederlands 🇳🇱](README.nl.md)

---

**X10 - Lights (Domotica Commander)** (`service.X10-lights`) is a Kodi / XBMC background service add-on that automatically switches, dims, or brightens home theater lighting and smart home devices based on media player and system events.

![XBMC Picture](docs/screenshots/XBMC%20picture.png)

---

## 📖 History & Background
This project was originally developed between **2011 and 2014** by **Majestic Soft** for a dedicated home cinema and published on the official XBMC/Kodi community forums.

The goal was to recreate the authentic, immersive cinema experience at home:
- As a movie begins, lights automatically and smoothly dim down;
- When playback is paused, lights turn on to a gentle ambient level for a break;
- When playback stops or finishes, full ambient lighting is restored.

This repository preserves both the **complete historical timeline (2011–2014)** from V0.0.1 through V1.0.4, as well as the modernized **V2.0.0 release** targeting modern Kodi versions (Python 3).

---

## ⚡ Key Features

- **Automated Event Triggers:**
  - `X_Start` – Kodi/XBMC startup (e.g. initialize room ambience)
  - `X_Stop` – Kodi/XBMC shutdown (e.g. turn all cinema lighting off)
  - `P_Start` – Video playback started (dim or turn lights off)
  - `P_Pause` – Video playback paused (raise lights to orientation/accent level)
  - `P_Resume` – Video playback resumed (dim lights back down)
  - `P_Stop` – Video playback stopped manually (restore ambient lights)
  - `P_End` – Video playback reached the end of title (restore lights)
- **Multi-Device Support:** Independently control up to **5 distinct devices or zones**.
- **Actions per Event:** Choose between `ON`, `OFF`, `DIM`, `BRIGHT` (0–100%) or customized *Free Commands*.
- **Bilingual Interface:** Fully localized settings in both **English** and **Dutch**.
- **Built-in Diagnostics:** Detailed debug logging option for easy troubleshooting.

---

## 🔌 Supported Domotica Platforms

| Domotica System | Protocol / Method | Description |
| :--- | :--- | :--- |
| **X10-Commander** | HTTP / API | Melloware X10-Commander device API calls |
| **HomeSeer** | HTTP POST REST | Direct HomeSeer device control |
| **tenHsServer** | HTTP GET | HomeSeer integration via tenHsServer extension |
| **Switch King** | HTTP REST | REST API calls to Switch King server |
| **Thinking Home** | HTTP GET | Thinking Home web server interface |
| **HomeWizard** | HTTP REST | Local HomeWizard HTTP API |
| **Domoticz** | HTTP JSON API | Domoticz switching and level dimming (0–16 scale) |
| **HomeGenie** | HTTP REST | HomeGenie API (contributed by Mack) |
| **LightWaveRF** | UDP Broadcast | Direct UDP socket broadcast to LightWaveRF WiFi Link |

---

## 🚀 What's New in V2.0.0 (Python 3 Migration)

- **Python 3 Compatibility:** Fully modernized for Kodi 19 Matrix, Kodi 20 Nexus, Kodi 21 Omega, and Kodi 22 Piers+.
- **Event-driven Monitor:** Replaced the legacy polling loop with `xbmc.Monitor().waitForAbort()`, enabling instant, zero-delay shutdown without CPU overhead.
- **Robust Network I/O:** Migrated `urllib`/`urllib2` to `urllib.request` and `urllib.parse` with strict 5-second timeouts to protect Kodi playback from freezing if a controller is offline.
- **UDP Bytes Encoding:** Safe payload byte-encoding (`utf-8`) for LightWaveRF UDP sockets.
- **Modern PO Translations:** Official gettext PO translation catalogs (`resource.language.en_gb` and `resource.language.nl_nl`).

---

## 📂 Repository Layout

```text
Proj_X10-Lights/
├── .gitignore               # Ignores python bytecode, caches, OS files & packages
├── LICENSE                  # GNU General Public License v2
├── README.md                # International English documentation (this file)
├── README.nl.md             # Dutch documentation
├── CHANGELOG.md             # Complete version history (v0.0.1 to v2.0.0)
├── docs/
│   ├── Manual - XBMC service.X10-lights (uk) R1.0.4.pdf   # Original 18-page manual
│   └── screenshots/         # Interface and configuration screenshots
└── service.X10-lights/      # The Kodi Add-on package folder
    ├── addon.xml            # Add-on metadata and service definition
    ├── default.py           # Python 3 service runtime logic
    ├── changelog.txt        # Add-on changelog
    ├── icon.png             # Add-on icon
    └── resources/
        ├── settings.xml     # Configuration menu schema
        └── language/        # Localization files (.po & .xml)
```

---

## 📸 Screenshots

| Categories | Device Settings |
| :---: | :---: |
| ![Settings 01](docs/screenshots/screenshot%2001.JPG) | ![Settings 02](docs/screenshots/screenshot%2002.JPG) |

| Event Configuration | Free Commands |
| :---: | :---: |
| ![Settings 03](docs/screenshots/screenshot%2003.JPG) | ![Settings 04](docs/screenshots/screenshot%2004.JPG) |

---

## 📚 Documentation
The original, comprehensive manual is available as a PDF in the `docs/` folder:
- 📄 [Manual - XBMC service.X10-lights (uk) R1.0.4.pdf](docs/Manual%20-%20XBMC%20service.X10-lights%20(uk)%20R1.0.4.pdf)

---

## 🛣️ Future Roadmap
- [ ] **Home Assistant:** Native Webhook and REST API integration for modern smart lights (Philips Hue, Zigbee, Z-Wave).
- [ ] **MQTT:** Publish Kodi playback and system events to an MQTT broker for universal smart home automation.
- [ ] **Asynchronous Event Queue:** Non-blocking threaded worker queue for all outgoing triggers.

---

## 📄 License
This project is licensed under the **GNU General Public License (GPL v2)** - see the [LICENSE](LICENSE) file for details.

**Author:** Majestic Soft  
**Email:** X10-Lights@majesticsoft.nl  
**Forum:** [Kodi Community Forum Topic](https://forum.kodi.tv/)
