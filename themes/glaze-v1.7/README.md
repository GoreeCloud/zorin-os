# GoreeCloud Glaze for Zorin OS

GoreeCloud Glaze is a from-scratch Zorin OS / GNOME theme package that maps the current Glaze V1.7 Stable/Anchor design semantics onto native Linux desktop surfaces.

## Status

- Theme package: 0.1.0-dev.1
- Lifecycle: Development
- Glaze target: Glaze V1.7 / 1.7.0
- Glaze authority verified at: 1a5756daed2294155be2e9972b24f580f6222b7b
- V1.7 source qualification anchor: 7c4ded83d7a8725165bb6a55dfb175667cc9589e
- Consumer/native acceptance: pending
- Primary current target: Zorin OS 18.1 Core/Pro (Ubuntu 24.04 base)
- Compatibility target: Zorin OS 17.3 Core/Pro (Ubuntu 22.04 base)

Glaze V1.7.0 is a bounded Stable release that inherits the accepted V1.6.0 runtime. This theme deliberately uses those Stable semantics and does not import retained dev.47 or Section 48 behavior that moved to V1.7.1.

## What is included

Two variants are included:

- GoreeCloud-Glaze — light-first desktop presentation.
- GoreeCloud-Glaze-Dark — dark desktop presentation.

Each variant provides GTK 3, GTK 4, and GNOME Shell CSS. The visual system uses the current Glaze semantic palette, coordinated radii, semantic focus, selection and state colors, bounded material depth, and solid readability-first content surfaces.

GTK and GNOME Shell do not provide one portable backdrop-blur contract across supported Zorin/GNOME versions. The theme therefore maps Glaze material to stable high-opacity surfaces, subtle depth, and semantic borders instead of depending on private compositor blur APIs. This is also a safe Reduced Transparency fallback.

## Install

Run:

    bash themes/glaze-v1.7/scripts/install.sh

This installs both variants into the current user's theme directory without changing the active theme.

To install and apply the GTK light variant:

    bash themes/glaze-v1.7/scripts/install.sh --apply light

To install and apply the GTK dark variant:

    bash themes/glaze-v1.7/scripts/install.sh --apply dark

The installer does not modify icon or cursor themes.

## GNOME Shell

The package includes GNOME Shell CSS, but applying a custom Shell theme requires a compatible User Themes extension. If that extension and its settings schema are available, run:

    bash themes/glaze-v1.7/scripts/install.sh --apply light --apply-shell

or:

    bash themes/glaze-v1.7/scripts/install.sh --apply dark --apply-shell

If the extension is not present, the installer leaves the Shell theme untouched and reports that condition.

## GTK 4 and libadwaita

The package ships a GTK 4 stylesheet for applications that honor GTK theme providers. Zorin OS 17 and newer can opt third-party GTK 4 themes into native libadwaita styling with a `.libadwaita` marker, but this Development package intentionally does not ship that marker yet. The opt-in remains gated on representative Zorin compatibility testing so native libadwaita applications are not themed before their widgets and accessibility behavior are verified.

## Accessibility and state design

The source maps Glaze semantic roles rather than treating the theme as a palette swap. It provides:

- explicit keyboard focus rings;
- separate accent, selection, information, success, warning, and danger roles;
- non-glass durable reading surfaces;
- light and dark semantic foregrounds;
- clear disabled states;
- bounded rounded geometry rather than uniform pill styling;
- no theme-authored decorative animation, so Reduced Motion does not have to disable theme-level motion;
- no dependency on blur for contrast or hierarchy.

Color remains a supporting signal; applications remain responsible for labels, icons, accessible names, and semantic status.

## Validation

Run:

    bash themes/glaze-v1.7/scripts/validate.sh

The validation checks package structure, Glaze V1.7 authority metadata, light/dark token mappings, brace balance, installer isolation, safe uninstall behavior, and the absence of unsupported/private blur dependencies.

Repository CI runs the same validator plus GTK 3 and GTK 4 parser checks for theme changes.

To build a deterministic Development archive locally, run:

    python3 themes/glaze-v1.7/scripts/build_package.py /tmp/goreecloud-glaze-build

The builder writes a `.tar.gz` package and matching SHA-256 file without changing the installed desktop theme.

## Current acceptance boundary

This source is implemented but remains Development until it receives representative Zorin OS native rendering and human/accessibility review. A green source-validation workflow does not by itself establish Glaze consumer acceptance, Zorin release acceptance, production readiness, or GoreeCloud OS Desktop conformance.

## Directory layout

- metadata/theme.json — exact Glaze target and acceptance boundary.
- variants/GoreeCloud-Glaze — light GTK/Shell variant.
- variants/GoreeCloud-Glaze-Dark — dark GTK/Shell variant.
- scripts/install.sh — user-scoped installer and optional theme application.
- scripts/uninstall.sh — guarded removal of only GoreeCloud-managed theme directories.
- scripts/validate.sh — deterministic source/package validation.


## Native acceptance

After extracting the Development package, run:

    bash scripts/native-preflight.sh

Then follow `NATIVE-ACCEPTANCE.md` for the light, dark, GTK, GNOME Shell, Zorin Taskbar, Zorin Menu, accessibility, rollback, and libadwaita acceptance sequence.

The preflight is read-only and does not establish visual or accessibility acceptance by itself.
