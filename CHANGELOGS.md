# GoreeCloud for Zorin OS — Changelogs

## 2026-10-03 — Glaze V1.7 Zorin theme source

- Added the new GoreeCloud Glaze theme package under `themes/glaze-v1.7/`.
- Added light-first `GoreeCloud-Glaze` and dark `GoreeCloud-Glaze-Dark` variants with GTK 3, GTK 4, and GNOME Shell presentation.
- Added `gtk-dark.css` paths so applications requesting dark presentation can retain the Glaze dark semantic palette even when the light desktop variant is selected.
- Bound the theme metadata to current Glaze V1.7 / 1.7.0 Stable/Anchor authority as verified at GoreeCloud/glaze revision `1a5756daed2294155be2e9972b24f580f6222b7b`.
- Preserved the V1.7 Stable boundary: retained dev.47 and Section 48 Development behavior are not imported into this theme.
- Defined Zorin OS 18.1 / Ubuntu 24.04 as the primary source-validation target and Zorin OS 17.3 / Ubuntu 22.04 as the compatibility target, without converting source-level checks into native rendered acceptance.
- Added semantic light/dark color roles, bounded surface depth, coordinated geometry, focus and selection states, disabled states, navigation surfaces, dialogs, menus, switches, progress, scrollbars, and GNOME Shell chrome.
- Added Zorin-specific GNOME Shell compatibility for the Zorin Taskbar and Zorin Menu while retaining the from-scratch GoreeCloud visual implementation.
- Added a guarded user-scoped installer, reversible uninstaller, deterministic source validator, and deterministic Development archive builder.
- Added GitHub Actions validation on Ubuntu 24.04 plus Ubuntu 22.04 compatibility parsing. Exact head `5283b55c8cf9e1817c4ff78535d0bfabd9eb948f` passed both jobs in workflow run `37157256520` and produced a reproducible Development archive.
- Preserved the generated archive as Actions artifact `11285403723`; its inner `goreecloud-glaze-zorin-0.1.0-dev.1.tar.gz` has SHA-256 `cdbf985a2472793ea0ca5071f83a52fca0624111e77da90fa54a18d4ae020148`. The Actions ZIP digest is `sha256:fee4e9560fd243bbe79a01347ca813c1aa72345329ce4738713ca38dfecf6080`.
- Kept the theme lifecycle at Development with native Zorin rendering, human visual/accessibility review, applied GNOME Shell review, libadwaita opt-in review, and downstream Glaze consumer acceptance still pending. Automated validation does not constitute Stable or production acceptance.

## 2026-09-27 — Care Drive feature-roadmap migration

- Moved Care feature authority from the synchronized Drive/repository roadmap model to repository-native `IMPLEMENTED-FEATURES.md`, `PLANNED-FEATURES.md`, and `CHANGELOGS.md`.
- Preserved CARE-001 through CARE-004 as planned/gated obligations without promoting lifecycle state.
- Retired the legacy repository `FEATURE-ROADMAP.md`; the Drive roadmap may be removed only after merge/readback.
