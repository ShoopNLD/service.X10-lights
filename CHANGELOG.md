# Changelog

All notable changes to the **X10 - Lights (Domotica Commander)** (`service.X10-lights`) project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.4] - 2014-04-06
### Added
- LightWaveRF support (controlling devices via UDP broadcast sockets).
### Changed
- `[CORE]` X10-Commander handling API calls updated to UDP broadcasts.
### Documentation
- Updated the comprehensive manual to revision 1.0.4.

---

## [1.0.3] - 2014-03-02
### Changed
- Updated Domoticz integration with DIM/BRIGHT functionality.
### Documentation
- Updated the manual.

---

## [1.0.2] - 2014-01-26
### Added
- HomeGenie support (contributed by Mack).
### Fixed
- Fixed language encoding issue in `addon.xml`.

---

## [1.0.1] - 2013-06-21
### Added
- Domoticz domotica server support.
### Fixed
- Fixed bug in HomeWizard HTTP API call.
### Changed
- Updated zip file packaging structure to directly support the *Install from zip file* option in XBMC/Kodi.
### Documentation
- Updated the manual.

---

## [1.0.1-dev] - 2013-05-08 *(Internal Build)*
### Changed
- `[CORE]` X10-Commander send calls refactoring.

---

## [1.0.0] - 2012-11-25
### Added
- Thinking Home support (via web server interface).
- HomeWizard support.
- Enable/Disable option for debug logging directly in settings.
### Changed
- Renamed project from *X10 Commander Lights* to *X10 - Lights (Domotica Commander)*.
- `[CORE]` Multi-device support: extended to control up to 5 independent devices/lights.
- `[CORE]` Improved event handling pipeline to seamlessly support multi-device configurations.
- `[CORE]` Removed default initialization actions for XBMC Start and Stop events.
### Documentation
- Updated manual to revision 1.0.0.

---

## [0.0.6-beta] - 2012-08-20 *(Internal Build)*
### Added
- Thinking Home web server integration prototype.
- `[CORE]` Multi-device support expansion (up to 5 devices).

---

## [0.0.6-alpha] - 2012-03-04
### Added
- Switch King domotica server support.
- Ability to Enable/Disable specific events per device.
- Predefined or custom free commands per event.
- Basic HTTP security authentication (username/password).
### Changed
- `[CORE]` Selection function adapted to handle free commands.
- `[CORE]` Application functions updated to parse and execute free commands.

---

## [0.0.5] - 2012-02-25
### Added
- `[CORE]` Modular selection function to dynamically route commands to dedicated controller handlers.
- Device actions (`ON` and `OFF`) added alongside dimming values.
- Prototype support for `tenHsServer`.
- Improved fault handling, error catching, and detailed event failure logging.
### Fixed
- Issue 1: Fixed crash on clean install when the add-on was not yet configured.
- Issue 2: Fixed XBMC Stop event execution.
### Changed
- `[CORE]` Decoupled X10-Commander handling into a dedicated function.
- `[CORE]` Decoupled HomeSeer handling into a dedicated function.

---

## [0.0.4] - 2011-09-25
### Changed
- Updated HomeSeer integration (removed intermediate `tenHsServer` requirement in favor of direct API).

---

## [0.0.3] - 2011-09-20
### Added
- HomeSeer integration via `tenHsServer`.

---

## [0.0.2] - 2011-09-18
### Added
- Categorized configuration menu in XBMC:
  - **HOST:** IP address and Port configuration.
  - **X10 Devices:** House code and target domotica application per device.
  - **XBMC Events:** Startup and Shutdown events (`DIM`/`BRIGHT` 0-100%).
  - **Player Events:** Play, Stop, End, Pause, Resume events (`DIM`/`BRIGHT` 0-100%).

---

## [0.0.1] - 2011-09-16
### Added
- Initial release of *X10 - Lights* for XBMC.
- Background service listening to XBMC playback events to automate room lighting.
- Initial support for X10-Commander (Melloware).
- Included English and Dutch user interface translations.
