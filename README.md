# Meshtastic Custom Builds (Overlay & Patch Architecture)

An automated, hands-off CI/CD pipeline for compiling custom [Meshtastic](https://github.com/meshtastic/firmware) firmware builds. This repository utilizes an **Overlay & Patch pattern** to automatically track upstream releases, compile both custom board variants and patched/PR-integrated builds on self-hosted GitHub Actions runners, store the compiled binaries in an organized tree committed to the repo, and automatically prune outdated release folders according to a defined retention policy.

---

## Architecture Overview

Rather than maintaining a heavy, diverging fork of the upstream `meshtastic/firmware` repository, this repository acts as a lightweight **control plane and overlay repository**:

```
meshtastic-custom-builds (This Repo)
  ├── build-config.yaml (Matrix Rules & Retention Policy)
  ├── variants/         (Custom board folders copied to firmware/variants/)
  └── patches/          (Local .patch files applied via git apply --3way)
            │
            ▼ (GitHub Actions Pipeline)
  ┌───────────────────────────────────────────────────────────────┐
  │ 1. Plan Job (ubuntu-latest): Queries upstream GitHub API,     │
  │    resolves active Alpha/Beta releases, generates build matrix│
  │                                                               │
  │ 2. Compile Job (self-hosted runner):                          │
  │    - Checks out upstream meshtastic/firmware at target tag    │
  │    - Overlays custom board variants                           │
  │    - Applies upstream PRs & local patches                     │
  │    - Runs PlatformIO build (pio run -e <env>)                 │
  │    - Emits build-manifest.json + firmware binaries            │
  │                                                               │
  │ 3. Publish & Prune Job (ubuntu-latest):                       │
  │    - Installs binaries into ./builds/<channel>-<tag>/...      │
  │    - Prunes expired release directories via retention policy  │
  │    - Generates ./builds/INDEX.md and commits back to main     │
  └───────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```text
meshtastic-custom-builds/
├── .github/
│   └── workflows/
│       └── build-pipeline.yml   # Multi-stage CI/CD pipeline (plan, compile, publish & prune)
├── build-config.yaml             # Single source of truth for build rules & retention
├── scripts/
│   ├── resolve_matrix.py         # Evaluates upstream releases and generates build matrix
│   └── prune_old_builds.py       # Prunes expired releases and updates builds/INDEX.md
├── variants/                     # Custom board definitions (copied to firmware/variants/)
│   └── .gitkeep
├── patches/                      # Local patch files (applied via git apply --3way)
│   └── .gitkeep
├── builds/                       # Committed repository output directory tree
│   ├── INDEX.md                  # Auto-generated catalog of all available firmware builds
│   └── .gitkeep
└── README.md                     # Documentation and usage guide
```

---

## Configuration: `build-config.yaml`

All build behavior, upstream tracking, board targets, and custom patches are managed in `build-config.yaml`.

```yaml
# ============================================================================
# 1. UPSTREAM TARGETING & RETENTION POLICY
# ============================================================================
release_channels:
  track_alpha: true               # Track latest Alpha release
  track_beta: true                # Track latest Beta release
  pinned_tags: []                 # Tags to always retain and build (e.g., ['v2.7.26.54e0d8d'])

retention:
  # Retain the N most recent releases per channel in ./builds/
  # Older folders outside of this window will be pruned during the publish step.
  keep_latest_alpha: 1
  keep_latest_beta: 1

# ============================================================================
# 2. BOARD VARIANTS
# ============================================================================
variants:
  custom:
    # Each entry corresponds to ./variants/<variant_dir>
    - name: "example-custom-s3"
      variant_dir: "example_custom_s3"
      pio_env: "example-custom-s3"
      build_vanilla: true         # Build unmodified upstream firmware for this custom board

  upstream:
    # Standard upstream PlatformIO environments
    - name: "heltec-v4"
      pio_env: "heltec-v4"
      build_vanilla: false        # Only build standard boards if targeted by custom profiles
    - name: "rak4631"
      pio_env: "rak4631"
      build_vanilla: false

# ============================================================================
# 3. CUSTOM BUILD PROFILES (PRs & Local Patches)
# ============================================================================
custom_profiles:
  - profile_name: "ble-and-telemetry-mods"
    enabled: false                # Toggle on/off
    description: "Upstream PRs + local modifications"
    upstream_prs:
      - 5432                      # Fetched from https://github.com/meshtastic/firmware/pull/5432.patch
    local_patches:
      - "01-example.patch"        # Located in ./patches/01-example.patch
    target_variants:
      - "all"                     # Options: ["all"], ["all_custom"], or ["example-custom-s3", "heltec-v4"]
```

---

## Adding Custom Board Variants

To add a proprietary or custom hardware variant:

1. Create a directory under `variants/`:
   ```bash
   mkdir -p variants/my_custom_board
   ```
2. Place the board definitions inside that directory, following Meshtastic's standard variant layout:
   - `platformio.ini` (declaring the board environment, build flags, and board configuration)
   - `variant.h` (pin definitions and hardware mapping)
   - Any auxiliary pin/peripheral headers
3. Add the variant to `variants.custom` in `build-config.yaml`:
   ```yaml
   variants:
     custom:
       - name: "my-custom-board"
         variant_dir: "my_custom_board"
         pio_env: "my-custom-board"
         build_vanilla: true
   ```
4. Push to `main`. The pipeline will automatically detect the new variant and compile it for active releases.

---

## Adding Patches and Upstream PRs

### Applying Upstream Pull Requests
If a feature or bugfix has been submitted as an upstream PR to `meshtastic/firmware` (e.g., PR `#10531`), add the PR number to `upstream_prs` inside a profile in `build-config.yaml`:

```yaml
custom_profiles:
  - profile_name: "pr-10531-test"
    enabled: true
    description: "Testing upstream PR 10531"
    upstream_prs:
      - 10531
    local_patches: []
    target_variants:
      - "rak4631"
      - "my-custom-board"
```
The runner will download `https://github.com/meshtastic/firmware/pull/<PR_NUM>.patch` and apply it with `git am --3way`.

### Applying Local Code Patches
For modifications not yet in a PR (or private custom tweaks):

1. Generate a patch against upstream `meshtastic/firmware`:
   ```bash
   git diff > patches/01-custom-telemetry.patch
   ```
2. Place the `.patch` file in `patches/`.
3. Reference it under `local_patches` in `build-config.yaml`:
   ```yaml
   custom_profiles:
     - profile_name: "telemetry-tweak"
       enabled: true
       upstream_prs: []
       local_patches:
         - "01-custom-telemetry.patch"
       target_variants:
         - "all_custom"
   ```
4. The runner will apply the patch using `git apply --3way`.

---

## Pipeline & Automation

The GitHub Actions workflow (`.github/workflows/build-pipeline.yml`) runs across three distinct triggers:

1. **Scheduled Polling (`cron: '0 */3 * * *'`):** Checks every 3 hours for new upstream Alpha or Beta firmware releases.
2. **Push Triggers:** Whenever `build-config.yaml`, `variants/**`, or `patches/**` are modified on `main`.
3. **Manual Trigger (`workflow_dispatch`):**
   - `force_tag`: Specify any arbitrary upstream tag (e.g., `v2.8.1.8e6a88d`) to build immediately.
   - `force_rebuild`: Force recompilation even if output folders already exist.

### Self-Hosted Runner Requirements
The `compile` job targets runners with labels:
```yaml
runs-on: [self-hosted, meshtastic-builder]
```

Prerequisites on the runner machine / container:
- **PlatformIO Core (`pio`):** Installed and accessible in `$PATH`.
- **Git & cURL:** Available in `$PATH`.
- **Python 3.10+:** Required by PlatformIO and build scripts.
- Hardware packages (ESP32, nRF52, RP2040 toolchains) will be automatically downloaded by PlatformIO on initial build.

---

## Output Structure & Artifacts

All compiled firmware binaries and manifest logs are committed into the repository under `./builds/`:

```text
builds/
├── INDEX.md                     # Markdown summary table of all active builds
├── alpha-v2.8.1.8e6a88d/
│   ├── vanilla/
│   │   └── example-custom-s3/
│   │       ├── build-manifest.json
│   │       ├── firmware-example-custom-s3-2.8.1.8e6a88d.bin
│   │       └── littlefs.bin
│   └── ble-and-telemetry-mods/
│       └── example-custom-s3/
│           ├── build-manifest.json
│           └── firmware-example-custom-s3-2.8.1.8e6a88d.bin
└── beta-v2.7.26.54e0d8d/
    └── vanilla/
        └── example-custom-s3/
            └── ...
```

### Build Manifest (`build-manifest.json`)
Every build variant produces a `build-manifest.json` capturing full provenance:
```json
{
  "tag": "v2.8.1.8e6a88d",
  "channel": "alpha",
  "build_type": "vanilla",
  "variant_name": "example-custom-s3",
  "pio_env": "example-custom-s3",
  "is_custom_variant": true,
  "variant_dir": "example_custom_s3",
  "upstream_prs": "",
  "local_patches": "",
  "upstream_commit": "8e6a88d4073380e2270bb3f0694efdb7bf71d791",
  "build_timestamp": "2026-11-02T16:20:00Z",
  "output_subpath": "builds/alpha-v2.8.1.8e6a88d/vanilla/example-custom-s3",
  "artifacts": [
    "firmware-example-custom-s3.bin"
  ]
}
```

---

## Local Script Testing

To test matrix resolution locally without triggering CI:

```bash
# Check upstream releases and preview pending matrix builds
python scripts/resolve_matrix.py

# Force build against a specific tag
python scripts/resolve_matrix.py --force-tag v2.8.1.8e6a88d --force-rebuild

# Test retention pruning and INDEX.md regeneration
python scripts/prune_old_builds.py
```
