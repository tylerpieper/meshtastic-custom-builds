#!/usr/bin/env python3
"""
prune_old_builds.py
Maintains the ./builds/ directory retention policy by removing release folders
not listed in active_folders, and generates/updates builds/INDEX.md summarizing
all currently retained builds, metadata, applied PRs/patches, and file links.
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_active_folders(
    active_folders_arg: Optional[str],
    repo_root: Path,
    config_path: Path,
) -> List[str]:
    """
    Parses active_folders from argument or environment variable.
    Falls back to recalculating via resolve_matrix if not provided.
    """
    raw = active_folders_arg or os.environ.get("ACTIVE_FOLDERS", "").strip()
    if raw:
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                return [str(item).strip() for item in data if str(item).strip()]
        except json.JSONDecodeError:
            try:
                import ast
                data = ast.literal_eval(raw)
                if isinstance(data, list):
                    return [str(item).strip() for item in data if str(item).strip()]
            except Exception as err:
                print(f"[WARN] Failed to parse active_folders JSON/literal: {err}. Recalculating...", file=sys.stderr)

    # Recalculate if not supplied
    try:
        from resolve_matrix import load_build_config, resolve_plan

        config = load_build_config(config_path)
        _, active_folders = resolve_plan(config=config, repo_root=repo_root)
        return active_folders
    except Exception as err:
        print(f"[WARN] Could not recalculate active_folders: {err}", file=sys.stderr)
        return []


def prune_outdated_folders(builds_dir: Path, active_folders: List[str]) -> List[str]:
    """Removes directories in builds/ that are not present in active_folders."""
    pruned: List[str] = []
    if not builds_dir.is_dir() or not active_folders:
        return pruned

    active_set = set(active_folders)

    for entry in builds_dir.iterdir():
        # Never prune special files or directories
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        if entry.name not in active_set:
            print(f"[PRUNE] Removing outdated release directory: {entry.name}")
            shutil.rmtree(entry)
            pruned.append(entry.name)

    return pruned


def scan_available_builds(builds_dir: Path) -> List[Dict[str, Any]]:
    """
    Scans the builds/ directory tree for all compiled variants and manifests.
    Expected hierarchy: builds/<release_folder>/<build_type>/<variant_name>/
    """
    builds: List[Dict[str, Any]] = []
    if not builds_dir.is_dir():
        return builds

    for release_dir in sorted(builds_dir.iterdir()):
        if not release_dir.is_dir() or release_dir.name.startswith("."):
            continue

        release_folder = release_dir.name
        # release_folder format is <channel>-<tag>, e.g. alpha-v2.8.1.8e6a88d
        parts = release_folder.split("-", 1)
        channel = parts[0] if len(parts) > 1 else "unknown"
        tag = parts[1] if len(parts) > 1 else release_folder

        for build_type_dir in sorted(release_dir.iterdir()):
            if not build_type_dir.is_dir() or build_type_dir.name.startswith("."):
                continue
            build_type = build_type_dir.name

            for variant_dir in sorted(build_type_dir.iterdir()):
                if not variant_dir.is_dir() or variant_dir.name.startswith("."):
                    continue
                variant_name = variant_dir.name

                manifest_file = variant_dir / "build-manifest.json"
                manifest_data: Dict[str, Any] = {}
                if manifest_file.is_file():
                    try:
                        with open(manifest_file, "r", encoding="utf-8") as f:
                            manifest_data = json.load(f)
                    except Exception as err:
                        print(f"[WARN] Failed to read {manifest_file}: {err}", file=sys.stderr)

                # Collect binary files
                binary_exts = {".bin", ".uf2", ".hex", ".elf"}
                binary_files = [
                    f.name for f in variant_dir.iterdir()
                    if f.is_file() and (f.suffix in binary_exts or f.name.endswith(".bin"))
                ]

                rel_folder_link = f"{release_folder}/{build_type}/{variant_name}"

                build_info = {
                    "release_folder": release_folder,
                    "channel": manifest_data.get("channel", channel),
                    "tag": manifest_data.get("tag", tag),
                    "build_type": manifest_data.get("build_type", build_type),
                    "variant_name": manifest_data.get("variant_name", variant_name),
                    "pio_env": manifest_data.get("pio_env", variant_name),
                    "upstream_prs": manifest_data.get("upstream_prs", ""),
                    "local_patches": manifest_data.get("local_patches", ""),
                    "upstream_commit": manifest_data.get("upstream_commit", ""),
                    "build_timestamp": manifest_data.get("build_timestamp", ""),
                    "relative_path": rel_folder_link,
                    "binaries": sorted(binary_files),
                }
                builds.append(build_info)

    return builds


def generate_index_markdown(builds: List[Dict[str, Any]], active_folders: List[str]) -> str:
    """Renders a comprehensive, clean INDEX.md file for the builds/ directory."""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines: List[str] = [
        "# Meshtastic Custom Firmware Builds Index",
        "",
        f"> **Last Pipeline Sync:** `{now_utc}`  ",
        f"> **Active Release Folders:** {', '.join(f'`{f}`' for f in sorted(active_folders)) if active_folders else '_None_'}",
        "",
        "This directory contains automated, overlay-patched firmware binaries compiled by the CI/CD pipeline.",
        "Outdated release directories not matching active retention rules are automatically pruned.",
        "",
        "---",
        "",
        "## Available Firmware Builds",
        "",
    ]

    if not builds:
        lines.extend([
            "_No firmware builds currently published._",
            "",
            "Builds will be published here automatically once the GitHub Actions runner completes a compile job.",
            "",
        ])
    else:
        lines.extend([
            "| Channel | Tag | Type | Variant | Target PIO Env | Applied PRs | Local Patches | Artifacts |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ])

        for b in builds:
            ch_badge = f"**{b['channel'].upper()}**" if b['channel'] in ('alpha', 'beta') else b['channel']
            tag_link = f"[`{b['tag']}`](https://github.com/meshtastic/firmware/releases/tag/{b['tag']})"
            prs_str = b['upstream_prs'] or "_None_"
            if b['upstream_prs']:
                prs_list = [
                    f"[#{pr}](https://github.com/meshtastic/firmware/pull/{pr})"
                    for pr in b['upstream_prs'].split()
                ]
                prs_str = ", ".join(prs_list)

            patches_str = f"`{b['local_patches']}`" if b['local_patches'] else "_None_"
            folder_link = f"[`{b['variant_name']}/`]({b['relative_path']}/)"

            # If specific binary files exist, link them
            if b['binaries']:
                bin_links = "<br>".join([
                    f"[`{fn}`]({b['relative_path']}/{fn})"
                    for fn in b['binaries']
                ])
                artifacts_cell = f"{folder_link}<br>{bin_links}"
            else:
                artifacts_cell = folder_link

            lines.append(
                f"| {ch_badge} | {tag_link} | `{b['build_type']}` | **{b['variant_name']}** | `{b['pio_env']}` | {prs_str} | {patches_str} | {artifacts_cell} |"
            )

        lines.extend([
            "",
            "---",
            "",
            "### Detailed Build Manifest Information",
            "",
            "Each variant directory includes a `build-manifest.json` file documenting the exact upstream git commit SHA, build timestamp, and applied modifications for provenance and reproducibility.",
            "",
        ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prune old Meshtastic builds and update INDEX.md")
    parser.add_argument("--active-folders", default=None, help="JSON list of active release folders to retain")
    parser.add_argument("--builds-dir", default="builds", help="Path to builds directory")
    parser.add_argument("--config", default="build-config.yaml", help="Path to build-config.yaml")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(repo_root / "scripts"))

    builds_dir = repo_root / args.builds_dir
    config_path = repo_root / args.config

    active_folders = load_active_folders(
        active_folders_arg=args.active_folders,
        repo_root=repo_root,
        config_path=config_path,
    )

    print("=" * 60)
    print("Meshtastic Build Retention & Pruning")
    print("=" * 60)
    print(f"Active Folders to Retain: {active_folders}")

    pruned = prune_outdated_folders(builds_dir=builds_dir, active_folders=active_folders)
    print(f"Pruned {len(pruned)} outdated folder(s): {pruned}")

    builds = scan_available_builds(builds_dir=builds_dir)
    print(f"Retained {len(builds)} available build variant(s)")

    index_content = generate_index_markdown(builds=builds, active_folders=active_folders)
    index_path = builds_dir / "INDEX.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    print(f"Successfully generated/updated {index_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
