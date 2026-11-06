# PR Build: pr-12084 - Station G3 LNA

> **Target Release:** `alpha-v2.8.2.4c89b69`  
> **Generated:** `2026-11-06 06:03:58 UTC`  
> **Profile Summary:** Software control for Station G3 discrete LNA via FEM interface  

---

## Upstream Pull Request Details

### [PR #12084: feat(station-g3): add software control for LNA via FEM interface](https://github.com/meshtastic/firmware/pull/12084)
* **Author:** [@tylerpieper](https://github.com/tylerpieper)
* **PR Link:** https://github.com/meshtastic/firmware/pull/12084

#### Description

## What changed
Added software control for the Station G3's discrete LNA via the existing `fem_lna_mode` configuration parameter, allowing users to override the LNA state dynamically without hardware jumpers.  

The Station G3 utilizes a discrete LNA on the primary slot (GPIO 10, Active LOW) that was previously only toggled by manually shorting or opening the "LNA P" hardware jumper. This leverages the existing `LoRaFEMInterface` in Meshtastic so that when `config.lora.fem_lna_mode = 1` (ENABLED), the LNA pin is pulled LOW during RX, and when it is `0` (DISABLED), the LNA pin is pulled HIGH.  

Software control requires that the jumper for the LNA be removed/open. If the jumper is installed/shorted, the LNA is disabled and cannot be enabled in software. See the [Utility Scripts section of the Station G3 quick start guide](https://wiki.bqvoy.com/en/devkits/station-g3#utility-scripts) for details on jumper behavior.

**Note on PA Control:** We are intentionally *not* implementing software control for the Station G3's PA Power Level (PA PL1) pin in this PR. Meshtastic currently lacks a generic protobuf configuration field to toggle discrete "PA High/Low Gain" states. Tying the Station G3's PA PL1 pin to the existing `LORA_PA_POWER` logic would be incorrect, as that logic asserts HIGH during both TX and RX windows, which would inappropriately force the PA rail into High Gain mode while listening. The PA power level configuration correctly remains hardware-jumper controlled.  I may be misunderstanding the code path here, so correct me if I am wrong.

## Changes made
- Defined `HAS_LORA_FEM=1`, `USE_STATION_G3_FEM=1`, and the `LORA_STATION_G3_LNA_EN` pin (10) for the `station-g3` variant in `platformio.ini` and `variant.h`.
- Registered `STATION_G3_FEM` in `LoRaFEMInterface` to enforce the correct Active LOW LNA state during `setRxModeEnable()` and disable it safely in `setTxModeEnable()` and `setSleepModeEnable()`.
- Added `#if defined(LORA_PA_POWER)` guards around the generic `enableFEMPower()` and `releaseSleepHolds()` functions in `LoRaFEMInterface.cpp`. Previously, this interface hardcoded the assumption that any board enabling the FEM would also define a `LORA_PA_POWER` pin (like the Heltec V4). These guards make the FEM interface modular, preventing compile failures for boards like the Station G3 that use the LNA features but do not define a generic FEM power pin.

## Testing
- **Compilation:** `station-g3` builds clean successfully with PlatformIO.
- **Hardware Verification:** Tested live on a Station G3 board with the physical LNA P jumper removed. Verified noise floor differences when toggling LNA mode via the Meshtastic configuration, confirming the software accurately asserts the pin during RX windows.

## 🤝 Attestations

- [X] I have tested that my proposed changes behave as described.
- [ ] I have tested that my proposed changes do not cause any obvious regressions on the following devices:
  - [ ] Heltec (Lora32) V3
  - [ ] LilyGo T-Deck
  - [ ] LilyGo T-Beam
  - [ ] RAK WisBlock 4631
  - [ ] Seeed Studio T-1000E tracker card
  - [ ] Other (please specify below)


<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

* **New Features**
  * Added Station G3 FEM support, including automatic LNA control for transmit, receive, and sleep states.
  * Configured Station G3 builds to enable LoRa FEM support.
<!-- end of auto-generated comment: release notes by coderabbit.ai -->

---

## Included Board Variants

| Variant | Files Available |
| :--- | :--- |
| [`station-g3/`](station-g3/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-station-g3-2.8.2.4c89b69.bin`, `firmware-station-g3-2.8.2.4c89b69.factory.bin`, `littlefs-station-g3-2.8.2.4c89b69.bin`, `mt-esp32s3-ota.bin` |
