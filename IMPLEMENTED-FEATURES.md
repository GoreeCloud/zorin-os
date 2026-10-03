# GoreeCloud for Zorin OS — Implemented Features

> **Authority:** Repository-native implemented-feature record for verified source that exists in this repository. Implementation does not imply release, Stable, production, or external-governance acceptance.

## Theme system

### THEME-001 — Glaze V1.7 native Zorin theme source

**Source state:** Implemented  
**Automated validation state:** Passing for the qualified theme payload; later documentation-only reconciliation does not change packaged theme bytes  
**Acceptance state:** Pending  
**Lifecycle:** Development

The repository contains a from-scratch GoreeCloud Glaze desktop theme under `themes/glaze-v1.7/` with:

- light and dark variants;
- GTK 3 styling;
- GTK 4 styling;
- GTK 3 and GTK 4 dark-preference stylesheets;
- GNOME Shell styling;
- Zorin Taskbar and Zorin Menu Shell compatibility selectors;
- Glaze V1.7 semantic light/dark color mapping;
- readability-first solid content surfaces and bounded translucent chrome;
- semantic focus, selection, success, information, warning, danger, and disabled states;
- coordinated Glaze geometry for controls, navigation, overlays, and transient surfaces;
- guarded user-scoped installation;
- reversible removal;
- deterministic source validation;
- deterministic Development archive construction;
- Ubuntu 24.04 source/parser validation for the Zorin OS 18.1 base target;
- Ubuntu 22.04 source/parser validation for the Zorin OS 17.3 compatibility target;
- exact-candidate GitHub Actions artifact preservation;\n- read-only native preflight helper and mandatory native acceptance checklist.

The implementation targets current Glaze V1.7 / 1.7.0 Stable/Anchor semantics and explicitly excludes retained dev.47 and Section 48 Development behavior transferred to V1.7.1.

Qualified theme-payload evidence:

- qualified payload source revision: `b2dc014e0231bfec373f111b264fa2402f105725`;
- workflow run: `37160036985`;
- Development artifact: `11287566536`;
- inner archive: `goreecloud-glaze-zorin-0.1.0-dev.1.tar.gz`;
- inner archive SHA-256: `8e2d067375d800399dad5db91ceb1df84c93ad02650b6977334e62b88784a5c8`;
- Actions ZIP digest: `sha256:24286349a46c85eee7fc3fb8197018780c704fec5c6ee7deab13eab98501a555`.

Representative Zorin OS native rendering, human visual review, accessibility review, applied GNOME Shell review, libadwaita opt-in acceptance, and downstream Glaze consumer acceptance remain separate gates and are not claimed by this implemented-source record.

## GoreeCloud Care

The migrated Care roadmap contains no CARE-001 through CARE-004 obligation classified as implemented or complete. Those obligations remain planned, gated, or blocked until their stated Stable evidence and promotion gates close.

Future implemented-feature claims must continue to be based on verified source and applicable evidence rather than plans alone.
