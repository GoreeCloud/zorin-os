# GoreeCloud Zorin — Glaze Originals Wallpaper Collection

## Status

Development. The collection is implemented as repository-native vector source and still requires exact-revision visual acceptance on the representative Zorin OS 17.3 target before release promotion.

The active wallpaper design system is **GLAZE UI V1.6 / 1.6.0 Official Anchor** through `config/palettes.json`. V1.7 remains Development and is not a consumer target for this collection.

## Product direction

The previous 24-wallpaper set was primarily identity/logo-derived. It is superseded by **Glaze Originals**, a new environmental wallpaper system designed to feel like part of Glaze UI without turning the desktop into a logo board.

The collection is intentionally:

- Glaze-native rather than logo-centric;
- quiet enough for desktop icons, windows, menus, docks, and text;
- visually varied by category while sharing one optical language;
- pure vector SVG with no downloaded stock photography;
- independent of semantic UI state colors;
- non-semantic: artwork never claims security, privacy, connectivity, health, or runtime state.

The user requested that no images be generated in chat. The implementation therefore lives entirely in repository source and is rendered by the wallpaper build pipeline.

## Scope

The repository defines exactly **30 3840×2160 SVG wallpapers**.

There are five categories, two distinct families in each category, and three appearance variants per family:

| Category | Families | Light | Dark | Deep Dark | Total |
| --- | --- | ---: | ---: | ---: | ---: |
| Atmosphere | Cirrus, Halo | 2 | 2 | 2 | 6 |
| Terrain | Tundra, Strata | 2 | 2 | 2 | 6 |
| Celestial | Orbit, Aurora | 2 | 2 | 2 | 6 |
| Architecture | Atrium, Vault | 2 | 2 | 2 | 6 |
| Digital | Mesh, Current | 2 | 2 | 2 | 6 |
| **Total** | **10 families** | **10** | **10** | **10** | **30** |

### Atmosphere

**Cirrus** uses layered translucent ribbons and long low-frequency curves to create a calm, airy desktop.

**Halo** uses broad optical glow and concentric frost rings with a restrained focal region.

### Terrain

**Tundra** abstracts frozen terrain into large crystalline horizon planes.

**Strata** uses topographic contour bands and quiet geological layering.

### Celestial

**Orbit** uses restrained orbital geometry and sparse luminous points.

**Aurora** uses broad translucent curtains rather than detailed sky imagery.

### Architecture

**Atrium** uses monumental frosted planes, open voids, and perspective edge light.

**Vault** uses repeated structural arcs and cool graphite depth.

### Digital

**Mesh** uses restrained network geometry and sparse nodes without implying live connectivity.

**Current** uses layered signal-like flows without representing data transfer or system status.

## Glaze UI visual contract

All ten compositions share these rules:

- use the V1.6 environmental base tokens for canvas, surface, elevated, deep, and border;
- use approved V1.6 optical references such as Frost White, Crystal White, Ice Blue, Glacier Blue, Clear Sky Blue, Cloud Gray, Slate Gray, and Graphite;
- keep major detail away from the central reading/work field where practical;
- prefer low-frequency geometry over texture noise;
- use translucent planes and edge light sparingly;
- preserve readable icon and panel contrast on representative target surfaces;
- avoid nested decorative complexity that competes with application content;
- avoid interaction/status semantics in environmental art.

Wallpaper templates may **not** consume focus, selection, destructive, warning, success, information, or other semantic UI-state tokens. The validator rejects those placeholders if introduced.

## Source model

Wallpaper definitions are stored in:

```text
config/wallpapers.json
```

The active schema is version 4 and records:

- exactly 30 catalog entries;
- exactly five categories;
- exactly two families per category;
- exactly three modes per family;
- the matching GoreeCloud Zorin appearance theme for each mode;
- the source template for every composition;
- V1.6 compatibility metadata.

The ten active source templates are:

```text
assets/wallpapers/templates/atmosphere-cirrus.svg.in
assets/wallpapers/templates/atmosphere-halo.svg.in
assets/wallpapers/templates/terrain-tundra.svg.in
assets/wallpapers/templates/terrain-strata.svg.in
assets/wallpapers/templates/celestial-orbit.svg.in
assets/wallpapers/templates/celestial-aurora.svg.in
assets/wallpapers/templates/architecture-atrium.svg.in
assets/wallpapers/templates/architecture-vault.svg.in
assets/wallpapers/templates/digital-mesh.svg.in
assets/wallpapers/templates/digital-current.svg.in
```

Older identity-oriented wallpaper templates and synchronized identity assets may remain temporarily as superseded repository provenance, but active generation and validation do not depend on them.

## Generation

Build all 30 wallpapers with:

```bash
python3 ./scripts/build_wallpapers.py --output /tmp/goreecloud-wallpapers
```

The builder reads the selected Glaze palette, injects only approved environmental and optical tokens into the ten templates, and produces three appearance variants for each composition.

The output must contain exactly 30 SVG files.

## GNOME / Zorin gallery behavior

Install or refresh the collection with:

```bash
./scripts/wallpaper.sh install
```

All 30 wallpapers are visible in GNOME Settings.

The gallery is **light-first, not light-only**:

1. 10 Light wallpapers
2. 10 Dark wallpapers
3. 10 Deep Dark wallpapers

Wallpaper choice is independent of the currently active desktop theme. A user may intentionally use a Dark or Deep Dark wallpaper with the Light application theme.

The default installer still applies the primary Light wallpaper, **Atmosphere — Cirrus — Light**.

Wallpaper files are installed user-locally under:

```text
~/.local/share/backgrounds/GoreeCloud-Zorin
```

The generated GNOME Background Properties catalog is installed under:

```text
~/.local/share/gnome-background-properties/goreecloud-zorin.xml
```

## Stock Zorin wallpaper replacement

The optional stock-replacement path continues to preserve Zorin packages and uses package-safe `dpkg-divert` handling for the exact audited Zorin OS 17.3 stock wallpaper files/catalogs.

It must never purge `zorin-os-artwork`, `zorin-os-desktop`, or their wallpaper dependencies merely to create a GoreeCloud-only gallery.

Use:

```bash
./scripts/wallpaper.sh replace-stock plan
./scripts/wallpaper.sh replace-stock apply
./scripts/wallpaper.sh replace-stock status
./scripts/wallpaper.sh replace-stock restore
```

## Validation

`python3 ./scripts/validate_wallpapers.py` enforces:

- manifest schema version 4;
- exactly 30 wallpapers;
- exactly five required categories;
- exactly six variants per category;
- exactly ten wallpapers per appearance mode;
- exactly two families per category;
- Light/Dark/Deep Dark coverage for every family;
- exactly ten active source templates;
- Glaze-native environmental role and art-direction metadata;
- absence of semantic UI-state tokens in wallpaper templates;
- absence of legacy identity-injection tokens in active templates;
- valid, local-only SVG with no script or external/data/file href resources;
- 3840×2160 dimensions and `0 0 3840 2160` viewBox;
- complete 30-entry GNOME catalog with no hidden GoreeCloud entries.

`python3 ./scripts/validate_light_catalog.py` verifies gallery ordering:

- 10 Light;
- 10 Dark;
- 10 Deep Dark;
- all 30 visible.

`python3 ./scripts/validate_v16_anchor.py` additionally requires the V1.6 build to produce exactly 30 wallpaper assets.

`python3 ./scripts/validate_system_wallpapers.py` requires the optional stock replacement path to expect exactly 30 GoreeCloud replacements while preserving the package-safety contract.

## Target acceptance

Source validation proves structure and reproducibility, not visual quality.

Before release promotion, test this exact collection on the representative Zorin OS 17.3 laptop and review:

- the complete 30-thumbnail Settings gallery;
- one representative wallpaper from each category in Light mode;
- representative Dark and Deep Dark compositions;
- desktop icon readability;
- panel/dock readability;
- window-edge contrast;
- bright and dark stress cases;
- 200% text scaling;
- increased-contrast or accessibility settings where applicable;
- wallpaper switching and settings persistence.

Any composition that is distracting, visually noisy, too logo-like, weak behind icons, or inconsistent with V1.6 should be corrected before the downstream Zorin theme leaves Development.
