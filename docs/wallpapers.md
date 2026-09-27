# GoreeCloud Zorin Wallpaper Collection

## Status

Development. Source implementation is identity-derived; target-device visual acceptance is pending for the redesigned artwork.

The earlier 24-wallpaper abstract collection was rejected during target review because its compositions did not match the current approved GoreeCloud, Glaze UI, Wardveil Security, and Privacy Shield artwork closely enough. That visual direction is superseded by the current identity-derived source and must not be treated as accepted wallpaper artwork.

The installed/default theme and wallpaper path now uses the repository's **GLAZE UI V1.6 / 1.6.0 Official Anchor** desktop adaptation in `config/palettes.json`. Downstream Zorin acceptance remains separate; the older V1.2 preview palette is retained only as migration provenance.

## Scope

The repository defines **24 3840×2160 SVG wallpapers** across four balanced categories:

| Category | Identity / families | Count |
| --- | --- | ---: |
| GoreeCloud | Unified Clean — Horizon, Meridian | 6 |
| Glaze UI | Facet — Aurora, Lattice | 6 |
| Wardveil Security | Sentinel Fold — Core, Veil | 6 |
| Privacy Shield | Approved Privacy Shield — Bands, Filter | 6 |
| **Total** | 8 families × Light/Dark/Deep Dark | **24** |

Every wallpaper preserves the canonical identity geometry and identity colors from the current unified branding authority. The surrounding field is intentionally environmental: neutral structure, low-frequency depth, restrained cold light, and generous quiet regions rather than a second brand mark or a semantic UI surface.

## Wallpaper visual contract

The redesigned source follows these rules:

- canonical marks keep their approved geometry and identity colors;
- GoreeCloud environmental light uses the approved platform blues rather than the theme's former Mineral Teal accent;
- Glaze UI, Wardveil Security, and Privacy Shield keep their own canonical identity color families;
- marks are subordinate to desktop work rather than oversized hero artwork;
- composition favors large calm regions, low-frequency detail, and restrained optical depth;
- wallpaper does not consume focus, selection, destructive, warning, or other semantic UI color tokens;
- changing the interactive theme accent must not silently recolor wallpaper identity artwork;
- wallpaper remains non-semantic and must not imply security, privacy, compliance, or runtime state.

This keeps family resemblance in the optical grammar while allowing every GoreeCloud identity to remain distinct.

## Branding authority and synchronization

Canonical identity authority is:

```text
GoreeCloud/goreecloud-branding-assets
```

The exact authority commit and synchronized source metadata are pinned in:

```text
config/wallpaper-identities.json
```

Synchronized consumer copies live under:

```text
assets/wallpapers/identity/
```

They are retained only so wallpaper generation works reproducibly and offline. They are not independent branding masters. The wallpaper builder verifies every synchronized SVG against its pinned SHA-256 before rendering.

Current canonical sources used by the wallpaper collection are:

- GoreeCloud Unified Clean transparent/reversed marks from `official/`;
- Glaze UI **Facet** from `systems/glaze-ui/glaze-ui-mark.svg`;
- Wardveil Security **Sentinel Fold** from `systems/wardveil-security/wardveil-security-icon.svg`;
- the approved Privacy Shield icon from `systems/privacy-shield/privacy-shield-icon.svg`.

GoreeCloud's official mark is never arbitrarily recolored or redrawn. Dark and Deep Dark wallpapers use the approved reversed variant. Glaze UI, Wardveil Security, and Privacy Shield preserve the identity colors already authored in their canonical SVGs. Glaze presentation effects may surround the marks without modifying their canonical geometry.

Wardveil Security and Privacy Shield artwork identifies those systems only. A wallpaper does not prove security protection, privacy state, runtime status, compliance, or production readiness.

## Generation

Wallpaper definitions are recorded in `config/wallpapers.json`. All 24 are generated from identity-aware templates under:

```text
assets/wallpapers/templates/
```

Build the current V1.6 Anchor-aligned collection with:

```bash
python3 ./scripts/build_wallpapers.py --output /tmp/goreecloud-wallpapers
```

The historical V1.2 preview can still be rendered for regression comparison with:

```bash
python3 ./scripts/build_wallpapers.py \
  --palette-config config/palettes-v1.2.json \
  --output /tmp/goreecloud-wallpapers-v1.2
```

The builder injects the verified canonical SVG interior into a nested SVG using the original canonical viewBox. It does not trace, approximate, recolor, or regenerate the logo geometry.

## Historical V1.2 preview boundary

`config/palettes-v1.2.json` is retained only as historical migration evidence. Current install, wallpaper, validation, and documentation paths use `config/palettes.json`, which records the V1.6 Official Anchor source pin and the downstream Zorin desktop adaptation.

Validate the preview contract with:

```bash
python3 ./scripts/validate_v16_anchor.py
```

That check validates the V1.6 Anchor/source pins, the Light/Dark/Deep Dark contract, semantic and focus contrast gates, desktop material/target floors, wallpaper alignment, and successful rendering of all theme and wallpaper variants. It remains a source gate only; target-device visual/accessibility acceptance is still required.

## User-local install and catalog

Run:

```bash
./scripts/wallpaper.sh install
./scripts/wallpaper.sh list
```

The helper installs all 24 SVGs under:

```text
~/.local/share/backgrounds/GoreeCloud-Zorin
```

and generates the user GNOME Background Properties catalog at:

```text
~/.local/share/gnome-background-properties/goreecloud-zorin.xml
```

Target evidence already confirms Zorin OS 17.3 Settings consumes this user-scoped catalog and displays the complete 24-entry collection. That discovery result applies to the catalog mechanism, not to visual acceptance of the redesigned artwork.

Apply the primary identity-derived wallpaper matching the active GoreeCloud theme with:

```bash
./scripts/wallpaper.sh apply current
```

Or apply any exact ID shown by `./scripts/wallpaper.sh list`.

Applying a wallpaper records a GNOME settings snapshot first. Restore the latest snapshot with:

```bash
./scripts/wallpaper.sh restore
```

## Stock Zorin wallpaper replacement

The desired end state is a GoreeCloud-only wallpaper gallery. Target testing showed that purging the four stock wallpaper packages is not safe: apt also proposes removing `zorin-os-artwork` and `zorin-os-desktop`, then installing Ubuntu wallpaper packages. The implementation therefore keeps every Zorin package installed.

Replacement now uses **local `dpkg-divert` entries** for the exact audited Zorin wallpaper images and GNOME background catalog files. Applying the replacement moves only those package-owned files from their normal `/usr/share/backgrounds` and `/usr/share/gnome-background-properties` locations into:

```text
/var/lib/goreecloud-zorin/stock-wallpaper-diversions
```

That makes the stock set disappear from GNOME/Zorin wallpaper discovery while preserving package ownership and desktop metapackages. Future package operations respect the diversions rather than restoring the stock files into the visible gallery.

Inspect the plan without changing the system:

```bash
./scripts/wallpaper.sh replace-stock plan
```

Apply it after the GoreeCloud collection is installed:

```bash
./scripts/wallpaper.sh replace-stock apply
```

Check status or restore the stock files:

```bash
./scripts/wallpaper.sh replace-stock status
./scripts/wallpaper.sh replace-stock restore
```

`finalize` removes the temporary recovery archive but deliberately leaves the package-safe diversions active. It does not purge Zorin packages.

The workflow verifies the exact Zorin OS 17.3 package versions and ownership evidence before making changes. It also records the unsafe apt purge simulation as diagnostic evidence, but there is no code path that executes that purge.

## Validation

`python3 ./scripts/validate_wallpapers.py` verifies:

- exactly 24 catalog entries across the four required categories;
- Light, Dark, and Deep Dark mappings;
- V1.6 Anchor/source-pin manifest metadata;
- pinned branding authority and synchronized canonical SVG SHA-256 values;
- canonical identity viewBoxes;
- identity/category mapping for every wallpaper;
- presence of canonical geometry in every rendered derivative;
- wallpaper source does not consume semantic interaction/status color tokens;
- 3840×2160 rendered dimensions and viewBox;
- no script elements or remote/file/data href resources;
- generated GNOME background catalog count and filenames.

`python3 ./scripts/validate_system_wallpapers.py` verifies that the stock replacement contract remains pinned to the exact audited Zorin package/file set, requires the `dpkg-divert` strategy, protects `zorin-os-artwork` and `zorin-os-desktop`, and rejects executable package-purge code.

Source validation proves reproducibility and identity-source integrity. It does not prove visual quality on the target display.

## Remaining target acceptance

Install the redesigned collection on the Zorin OS 17.3 laptop, reopen Settings → Background, review the 24 thumbnails and representative full-desktop renders, and verify that Unified Clean, Facet, Sentinel Fold, and Privacy Shield are visibly faithful to their canonical artwork in Light/Dark/Deep Dark contexts.

For the current V1.6 adaptation, review the same representative set against the Frost/Graphite environment and include bright, dark, saturated, and detailed wallpaper stress cases, increased contrast, reduced transparency where applicable, and 200% text before any release promotion.
