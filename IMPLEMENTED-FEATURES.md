# GoreeCloud for Zorin OS — Implemented Features

> **Authority:** Repository-native implemented-feature record for verified source that exists in this repository. Implementation does not imply release, Stable, production, or external-governance acceptance.

## Theme system

### THEME-001 — Glaze V1.7 native Zorin theme source

**Source state:** Implemented  
**Acceptance state:** Pending  
**Lifecycle:** Development

The repository contains a from-scratch GoreeCloud Glaze desktop theme under `themes/glaze-v1.7/` with:

- light and dark variants;
- GTK 3 styling;
- GTK 4 styling;
- GNOME Shell styling;
- Glaze V1.7 semantic light/dark color mapping;
- readability-first solid content surfaces and bounded translucent chrome;
- semantic focus, selection, success, information, warning, danger, and disabled states;
- coordinated Glaze geometry for controls, navigation, overlays, and transient surfaces;
- guarded user-scoped installation;
- reversible removal;
- deterministic source/package validation;
- repository CI for exact theme-source validation.

The implementation targets current Glaze V1.7 / 1.7.0 Stable/Anchor semantics and explicitly excludes retained dev.47 and Section 48 Development behavior transferred to V1.7.1.

Representative Zorin OS native rendering, human visual review, accessibility review, Shell-extension compatibility, and consumer acceptance remain separate gates and are not claimed by this implemented-source record.

## GoreeCloud Care

The migrated Care roadmap contains no CARE-001 through CARE-004 obligation classified as implemented or complete. Those obligations remain planned, gated, or blocked until their stated Stable evidence and promotion gates close.

Future implemented-feature claims must continue to be based on verified source and applicable evidence rather than plans alone.
