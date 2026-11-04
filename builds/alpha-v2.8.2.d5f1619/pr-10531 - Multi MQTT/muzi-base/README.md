# PR Build: pr-10531 - Multi MQTT

> **Target Release:** `alpha-v2.8.2.d5f1619`  
> **Generated:** `2026-11-04 06:59:09 UTC`  
> **Profile Summary:** Allow MQTT uplinks to uplink multiple copies of packets  

---

## Upstream Pull Request Details

### [PR #10531: Add a way to have MQTT uplinks uplink multiple copies of packets](https://github.com/meshtastic/firmware/pull/10531)
* **Author:** [@ianmcorvidae](https://github.com/ianmcorvidae)
* **PR Link:** https://github.com/meshtastic/firmware/pull/10531

#### Description

... when they're heard multiple times (hidden behind compile flag + userPrefs)

This is entirely for MQTT-based analytics. Uplinking packets multiple times means analytics tools and users can see SNRs for rebroadcasts after the first heard by each uplink, and it's especially useful for traceroutes, where entire paths that might otherwise not appear can come by way of later-heard copies of the packet.

My experience level with C++ is not amazing so I'm suspecting there are things here that aren't needed, despite my best efforts to rein in the generated code. The primary parts of this PR are just moving MQTT uplink logic into a dedicated `Router::publishReceivedToMqtt` and then calling it from a variety of places to catch packets that otherwise wouldn't make it to the regular uplink location.

Some specific question areas are the necessity of lines 870-874 in Router.cpp, serving as a dummy implementation I guess, and whether the gate on MQTT being enabled at all should be moved to live outside the newly created function. I'll try to test it on a few more devices, but it's also not a huge change and it works on at least one esp32 and nrf52, so I'm not too worried it'll turn up issues.

## 🤝 Attestations

- [x] I have tested that my proposed changes behave as described.
- [ ] I have tested that my proposed changes do not cause any obvious regressions on the following devices:
  - [ ] Heltec (Lora32) V3
  - [ ] LilyGo T-Deck
  - [ ] LilyGo T-Beam
  - [ ] RAK WisBlock 4631
  - [x] Seeed Studio T-1000E tracker card
  - [x] Other (please specify below) (LilyGo t3s3 v1)

---

## Included Board Variants

| Variant | Files Available |
| :--- | :--- |
| [`axiometa-genesis-mini/`](axiometa-genesis-mini/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-axiometa-genesis-mini-2.8.2.d5f1619.bin`, `firmware-axiometa-genesis-mini-2.8.2.d5f1619.factory.bin`, `littlefs-axiometa-genesis-mini-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`chatter2/`](chatter2/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-chatter2-2.8.2.d5f1619.bin`, `firmware-chatter2-2.8.2.d5f1619.factory.bin`, `littlefs-chatter2-2.8.2.d5f1619.bin`, `mt-esp32-ota.bin` |
| [`heltec-mesh-pocket-10000/`](heltec-mesh-pocket-10000/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-heltec-mesh-pocket-10000-2.8.2.d5f1619-ota.zip`, `firmware-heltec-mesh-pocket-10000-2.8.2.d5f1619.hex`, `firmware-heltec-mesh-pocket-10000-2.8.2.d5f1619.uf2` |
| [`heltec-mesh-pocket-5000/`](heltec-mesh-pocket-5000/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-heltec-mesh-pocket-5000-2.8.2.d5f1619-ota.zip`, `firmware-heltec-mesh-pocket-5000-2.8.2.d5f1619.hex`, `firmware-heltec-mesh-pocket-5000-2.8.2.d5f1619.uf2` |
| [`heltec-mesh-tower-v2/`](heltec-mesh-tower-v2/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-heltec-mesh-tower-v2-2.8.2.d5f1619-ota.zip`, `firmware-heltec-mesh-tower-v2-2.8.2.d5f1619.hex`, `firmware-heltec-mesh-tower-v2-2.8.2.d5f1619.uf2` |
| [`heltec-t096/`](heltec-t096/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-heltec-mesh-node-t096-2.8.2.d5f1619-ota.zip`, `firmware-heltec-mesh-node-t096-2.8.2.d5f1619.hex`, `firmware-heltec-mesh-node-t096-2.8.2.d5f1619.uf2` |
| [`heltec-t1/`](heltec-t1/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-heltec-mesh-node-t1-2.8.2.d5f1619-ota.zip`, `firmware-heltec-mesh-node-t1-2.8.2.d5f1619.hex`, `firmware-heltec-mesh-node-t1-2.8.2.d5f1619.uf2` |
| [`heltec-t114/`](heltec-t114/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-heltec-mesh-node-t114-2.8.2.d5f1619-ota.zip`, `firmware-heltec-mesh-node-t114-2.8.2.d5f1619.hex`, `firmware-heltec-mesh-node-t114-2.8.2.d5f1619.uf2` |
| [`heltec-v3/`](heltec-v3/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-heltec-v3-2.8.2.d5f1619.bin`, `firmware-heltec-v3-2.8.2.d5f1619.factory.bin`, `littlefs-heltec-v3-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`heltec-v4/`](heltec-v4/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-heltec-v4-2.8.2.d5f1619.bin`, `firmware-heltec-v4-2.8.2.d5f1619.factory.bin`, `littlefs-heltec-v4-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`heltec-v4-tft/`](heltec-v4-tft/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-heltec-v4-tft-2.8.2.d5f1619.bin`, `firmware-heltec-v4-tft-2.8.2.d5f1619.factory.bin`, `littlefs-heltec-v4-tft-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`heltec-v4r8/`](heltec-v4r8/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-heltec-v4-r8-oled-2.8.2.d5f1619.bin`, `firmware-heltec-v4-r8-oled-2.8.2.d5f1619.factory.bin`, `littlefs-heltec-v4-r8-oled-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`heltec-v4r8-tft/`](heltec-v4r8-tft/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-heltec-v4-r8-tft-2.8.2.d5f1619.bin`, `firmware-heltec-v4-r8-tft-2.8.2.d5f1619.factory.bin`, `littlefs-heltec-v4-r8-tft-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`heltec-wireless-tracker-v2/`](heltec-wireless-tracker-v2/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-heltec-wireless-tracker-v2-2.8.2.d5f1619.bin`, `firmware-heltec-wireless-tracker-v2-2.8.2.d5f1619.factory.bin`, `littlefs-heltec-wireless-tracker-v2-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`m5stack-cardputer-adv/`](m5stack-cardputer-adv/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-m5stack-cardputer-adv-2.8.2.d5f1619.bin`, `firmware-m5stack-cardputer-adv-2.8.2.d5f1619.factory.bin`, `littlefs-m5stack-cardputer-adv-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`meshtiny/`](meshtiny/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-meshtiny-2.8.2.d5f1619-ota.zip`, `firmware-meshtiny-2.8.2.d5f1619.hex`, `firmware-meshtiny-2.8.2.d5f1619.uf2` |
| [`muzi-base/`](muzi-base/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-muzi-base-2.8.2.d5f1619-ota.zip`, `firmware-muzi-base-2.8.2.d5f1619.hex`, `firmware-muzi-base-2.8.2.d5f1619.uf2` |
| [`picomputer-s3/`](picomputer-s3/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-picomputer-s3-2.8.2.d5f1619.bin`, `firmware-picomputer-s3-2.8.2.d5f1619.factory.bin`, `littlefs-picomputer-s3-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`picomputer-s3-tft/`](picomputer-s3-tft/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-picomputer-s3-tft-2.8.2.d5f1619.bin`, `firmware-picomputer-s3-tft-2.8.2.d5f1619.factory.bin`, `littlefs-picomputer-s3-tft-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`portduino/`](portduino/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh` |
| [`rak-wismeshtag/`](rak-wismeshtag/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-rak_wismeshtag-2.8.2.d5f1619-ota.zip`, `firmware-rak_wismeshtag-2.8.2.d5f1619.hex`, `firmware-rak_wismeshtag-2.8.2.d5f1619.uf2` |
| [`rak3401-1watt/`](rak3401-1watt/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-rak3401-1watt-2.8.2.d5f1619-ota.zip`, `firmware-rak3401-1watt-2.8.2.d5f1619.hex`, `firmware-rak3401-1watt-2.8.2.d5f1619.uf2` |
| [`rak4631/`](rak4631/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-rak4631-2.8.2.d5f1619-ota.zip`, `firmware-rak4631-2.8.2.d5f1619.hex`, `firmware-rak4631-2.8.2.d5f1619.uf2` |
| [`seeed-p1-pro/`](seeed-p1-pro/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-seeed_solar_node-2.8.2.d5f1619-ota.zip`, `firmware-seeed_solar_node-2.8.2.d5f1619.hex`, `firmware-seeed_solar_node-2.8.2.d5f1619.uf2` |
| [`solarxiao_e22p/`](solarxiao_e22p/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-seeed_xiao_nrf52840_kit-v2.8.2.d5f1619-ota.zip`, `firmware-solarxiao_e22p-2.8.2.d5f1619-ota.zip`, `firmware-solarxiao_e22p-2.8.2.d5f1619.hex`, `firmware-solarxiao_e22p-2.8.2.d5f1619.uf2` |
| [`spicy_e22p_i2c/`](spicy_e22p_i2c/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-seeed_xiao_nrf52840_kit-v2.8.2.d5f1619-ota.zip`, `firmware-spicy_e22p_i2c-2.8.2.d5f1619-ota.zip`, `firmware-spicy_e22p_i2c-2.8.2.d5f1619.hex`, `firmware-spicy_e22p_i2c-2.8.2.d5f1619.uf2` |
| [`spicy_m33_i2c/`](spicy_m33_i2c/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-seeed_xiao_nrf52840_kit-v2.8.2.d5f1619-ota.zip`, `firmware-spicy_m33_i2c-2.8.2.d5f1619-ota.zip`, `firmware-spicy_m33_i2c-2.8.2.d5f1619.hex`, `firmware-spicy_m33_i2c-2.8.2.d5f1619.uf2` |
| [`station-g2/`](station-g2/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-station-g2-2.8.2.d5f1619.bin`, `firmware-station-g2-2.8.2.d5f1619.factory.bin`, `littlefs-station-g2-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`station-g3/`](station-g3/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-station-g3-2.8.2.d5f1619.bin`, `firmware-station-g3-2.8.2.d5f1619.factory.bin`, `littlefs-station-g3-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`t-beam-1w/`](t-beam-1w/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-t-beam-1w-2.8.2.d5f1619.bin`, `firmware-t-beam-1w-2.8.2.d5f1619.factory.bin`, `littlefs-t-beam-1w-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`t-deck/`](t-deck/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-t-deck-2.8.2.d5f1619.bin`, `firmware-t-deck-2.8.2.d5f1619.factory.bin`, `littlefs-t-deck-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`t-deck-tft/`](t-deck-tft/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-t-deck-tft-2.8.2.d5f1619.bin`, `firmware-t-deck-tft-2.8.2.d5f1619.factory.bin`, `littlefs-t-deck-tft-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`t-echo/`](t-echo/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-t-echo-2.8.2.d5f1619-ota.zip`, `firmware-t-echo-2.8.2.d5f1619.hex`, `firmware-t-echo-2.8.2.d5f1619.uf2` |
| [`tbeam/`](tbeam/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-tbeam-2.8.2.d5f1619.bin`, `firmware-tbeam-2.8.2.d5f1619.factory.bin`, `littlefs-tbeam-2.8.2.d5f1619.bin`, `mt-esp32-ota.bin` |
| [`tbeam-s3-core/`](tbeam-s3-core/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-tbeam-s3-core-2.8.2.d5f1619.bin`, `firmware-tbeam-s3-core-2.8.2.d5f1619.factory.bin`, `littlefs-tbeam-s3-core-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`tlora-pager/`](tlora-pager/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-tlora-pager-2.8.2.d5f1619.bin`, `firmware-tlora-pager-2.8.2.d5f1619.factory.bin`, `littlefs-tlora-pager-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`tlora-t3s3/`](tlora-t3s3/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-tlora-t3s3-v1-2.8.2.d5f1619.bin`, `firmware-tlora-t3s3-v1-2.8.2.d5f1619.factory.bin`, `littlefs-tlora-t3s3-v1-2.8.2.d5f1619.bin`, `mt-esp32s3-ota.bin` |
| [`tracker-t1000e/`](tracker-t1000e/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-tracker-t1000-e-2.8.2.d5f1619-ota.zip`, `firmware-tracker-t1000-e-2.8.2.d5f1619.hex`, `firmware-tracker-t1000-e-2.8.2.d5f1619.uf2` |
| [`tracker-x1/`](tracker-x1/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-seeed_mesh_tracker_X1-2.8.2.d5f1619-ota.zip`, `firmware-seeed_mesh_tracker_X1-2.8.2.d5f1619.hex`, `firmware-seeed_mesh_tracker_X1-2.8.2.d5f1619.uf2` |
| [`wio-tracker-l1/`](wio-tracker-l1/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-seeed_wio_tracker_L1-2.8.2.d5f1619-ota.zip`, `firmware-seeed_wio_tracker_L1-2.8.2.d5f1619.hex`, `firmware-seeed_wio_tracker_L1-2.8.2.d5f1619.uf2` |
| [`wio-tracker-l1-pro-1w/`](wio-tracker-l1-pro-1w/) | `device-install.bat`, `device-install.sh`, `device-update.bat`, `device-update.sh`, `firmware-seeed_wio_tracker_L1_Pro_1W-2.8.2.d5f1619-ota.zip`, `firmware-seeed_wio_tracker_L1_Pro_1W-2.8.2.d5f1619.hex`, `firmware-seeed_wio_tracker_L1_Pro_1W-2.8.2.d5f1619.uf2` |
