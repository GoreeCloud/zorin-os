# GoreeCloud for Zorin OS — Changelogs

## 2026-10-03 — Glaze V1.7 Zorin theme source

- Added the new GoreeCloud Glaze theme package under `themes/glaze-v1.7/`.
- Added light-first `GoreeCloud-Glaze` and dark `GoreeCloud-Glaze-Dark` variants with GTK 3, GTK 4, and GNOME Shell presentation.
- Bound the theme metadata to current Glaze V1.7 / 1.7.0 Stable/Anchor authority as verified at GoreeCloud/glaze revision `1a5756daed2294155be2e9972b24f580f6222b7b`.
- Preserved the V1.7 Stable boundary: retained dev.47 and Section 48 Development behavior are not imported into this theme.
- Added semantic light/dark color roles, bounded surface depth, coordinated geometry, focus and selection states, disabled states, navigation surfaces, dialogs, menus, switches, progress, scrollbars, and GNOME Shell chrome.
- Added a guarded user-scoped installer, reversible uninstaller, deterministic source validator, and GitHub Actions validation workflow.
- Kept the theme lifecycle at Development with native Zorin rendering, human visual/accessibility review, and consumer acceptance still pending. Source implementation and automated validation do not constitute Stable or production acceptance.

## 2026-09-27 — Care Drive feature-roadmap migration

- Moved Care feature authority from the synchronized Drive/repository roadmap model to repository-native `IMPLEMENTED-FEATURES.md`, `PLANNED-FEATURES.md`, and `CHANGELOGS.md`.
- Preserved CARE-001 through CARE-004 as planned/gated obligations without promoting lifecycle state.
- Retired the legacy repository `FEATURE-ROADMAP.md`; the Drive roadmap may be removed only after merge/readback.
