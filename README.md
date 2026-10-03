# GoreeCloud for Zorin OS

GoreeCloud's Zorin OS integration repository contains desktop themes, workstation-specific assets, applications, packaging, validation tooling, and related platform work for GoreeCloud on Zorin OS.

## Current status

This repository is an active Development workspace. Individual components may have their own lifecycle and acceptance state; a merge or green CI run does not by itself establish Stable, production, or GoreeCloud OS Desktop acceptance.

## Glaze V1.7 theme

The repository now includes a from-scratch **GoreeCloud Glaze** desktop theme under [`themes/glaze-v1.7/`](themes/glaze-v1.7/).

Current theme scope:

- `GoreeCloud-Glaze` light-first variant.
- `GoreeCloud-Glaze-Dark` dark variant.
- GTK 3 and GTK 4 styling.
- GNOME Shell styling.
- Glaze V1.7 semantic color, geometry, focus, selection, state, material, and depth mapping.
- Guarded user-scoped installation and reversible removal.
- Exact-source validation and GTK parser CI.
- Deterministic Development archive tooling.

The theme currently remains **Development**. Representative Zorin native rendering, human visual/accessibility review, Shell compatibility review, and downstream Glaze consumer acceptance remain separate gates.

See [the theme README](themes/glaze-v1.7/README.md) for installation, validation, compatibility, and acceptance details.

## GoreeCloud Care

GoreeCloud Care is maintained under [`apps/goreecloud-care/`](apps/goreecloud-care/) as a first-party local maintenance application. Its lifecycle, release, and platform-integration evidence remain independent from the desktop-theme lifecycle.

## Repository records

Repository-native feature and change records currently include:

- [Implemented features](IMPLEMENTED-FEATURES.md)
- [Planned features](PLANNED-FEATURES.md)
- [Changelogs](CHANGELOGS.md)

These records distinguish implemented source from acceptance, release, deployment, and Stable lifecycle state.

## Source-control boundary

GitHub is the authoritative source-control location for this repository. Development changes should remain traceable to exact commits, reviewed branches, CI evidence, and applicable acceptance records.
