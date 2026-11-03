# Meshtastic Custom Firmware Builds Index

> **Last Pipeline Sync:** `2026-11-03 19:19:53 UTC`  
> **Active Release Folders:** `alpha-v2.8.1.8e6a88d`, `alpha-v2.8.2.4c89b69`, `beta-v2.7.26.54e0d8d`

This directory contains automated, overlay-patched firmware binaries compiled by the CI/CD pipeline.
Outdated release directories not matching active retention rules are automatically pruned.

---

## Available Firmware Builds

| Channel | Tag | Type | Variant | Target PIO Env | Applied PRs | Local Patches | Artifacts |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ALPHA** | [`v2.8.1.8e6a88d`](https://github.com/meshtastic/firmware/releases/tag/v2.8.1.8e6a88d) | `vanilla` | **spicy_e22p_i2c** | `spicy_e22p_i2c` | _None_ | _None_ | [`spicy_e22p_i2c/`](alpha-v2.8.1.8e6a88d/vanilla/spicy_e22p_i2c/)<br>[`firmware-spicy_e22p_i2c-2.8.1.8e6a88d-ota.zip`](alpha-v2.8.1.8e6a88d/vanilla/spicy_e22p_i2c/firmware-spicy_e22p_i2c-2.8.1.8e6a88d-ota.zip)<br>[`firmware-spicy_e22p_i2c-2.8.1.8e6a88d.hex`](alpha-v2.8.1.8e6a88d/vanilla/spicy_e22p_i2c/firmware-spicy_e22p_i2c-2.8.1.8e6a88d.hex)<br>[`firmware-spicy_e22p_i2c-2.8.1.8e6a88d.uf2`](alpha-v2.8.1.8e6a88d/vanilla/spicy_e22p_i2c/firmware-spicy_e22p_i2c-2.8.1.8e6a88d.uf2) |
| **ALPHA** | [`v2.8.1.8e6a88d`](https://github.com/meshtastic/firmware/releases/tag/v2.8.1.8e6a88d) | `vanilla` | **spicy_m33_i2c** | `spicy_m33_i2c` | _None_ | _None_ | [`spicy_m33_i2c/`](alpha-v2.8.1.8e6a88d/vanilla/spicy_m33_i2c/)<br>[`firmware-spicy_m33_i2c-2.8.1.8e6a88d-ota.zip`](alpha-v2.8.1.8e6a88d/vanilla/spicy_m33_i2c/firmware-spicy_m33_i2c-2.8.1.8e6a88d-ota.zip)<br>[`firmware-spicy_m33_i2c-2.8.1.8e6a88d.hex`](alpha-v2.8.1.8e6a88d/vanilla/spicy_m33_i2c/firmware-spicy_m33_i2c-2.8.1.8e6a88d.hex)<br>[`firmware-spicy_m33_i2c-2.8.1.8e6a88d.uf2`](alpha-v2.8.1.8e6a88d/vanilla/spicy_m33_i2c/firmware-spicy_m33_i2c-2.8.1.8e6a88d.uf2) |
| **BETA** | [`v2.7.26.54e0d8d`](https://github.com/meshtastic/firmware/releases/tag/v2.7.26.54e0d8d) | `vanilla` | **spicy_e22p_i2c** | `spicy_e22p_i2c` | _None_ | _None_ | [`spicy_e22p_i2c/`](beta-v2.7.26.54e0d8d/vanilla/spicy_e22p_i2c/)<br>[`firmware-spicy_e22p_i2c-2.7.26.54e0d8d.uf2`](beta-v2.7.26.54e0d8d/vanilla/spicy_e22p_i2c/firmware-spicy_e22p_i2c-2.7.26.54e0d8d.uf2) |
| **BETA** | [`v2.7.26.54e0d8d`](https://github.com/meshtastic/firmware/releases/tag/v2.7.26.54e0d8d) | `vanilla` | **spicy_m33_i2c** | `spicy_m33_i2c` | _None_ | _None_ | [`spicy_m33_i2c/`](beta-v2.7.26.54e0d8d/vanilla/spicy_m33_i2c/)<br>[`firmware-spicy_m33_i2c-2.7.26.54e0d8d.uf2`](beta-v2.7.26.54e0d8d/vanilla/spicy_m33_i2c/firmware-spicy_m33_i2c-2.7.26.54e0d8d.uf2) |

---

### Detailed Build Manifest Information

Each variant directory includes a `build-manifest.json` file documenting the exact upstream git commit SHA, build timestamp, and applied modifications for provenance and reproducibility.
