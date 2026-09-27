# Glaze UI V1.2 Preview — Zorin OS

> **Historical migration record.** The current default desktop contract is GLAZE UI V1.6 / 1.6.0 Official Anchor in `config/palettes.json`. This document is retained only to explain the earlier V1.2 preview path and must not be used as current lifecycle or installation guidance.

## Status

**Development preview. Not Stable.**

The accepted predecessor remains Glaze UI V1.1 / 1.1.0. This preview exists so V1.2 can be implemented and tested without silently transferring V1.1 acceptance to materially different color, material, wallpaper, or accessibility behavior.

The target platform remains Zorin OS 17.3 with the existing GTK 2 compatibility shim, GTK 3 theme, GTK 4/libadwaita opt-in path, and GNOME Shell mapping.

## V1.2 visual direction

The preview translates the proposed Glaze UI V1.2 identity into the desktop environment as:

**Frost White + Ice Blue + Clear Translucency + Cool Graphite**

The implementation principle is that material and structure carry the identity more strongly than saturated color:

- white behaves as light;
- blue behaves as atmosphere;
- translucency behaves as depth where the platform safely supports it;
- graphite provides durable structure;
- semantic state remains isolated from wallpaper/environmental color.

## Machine-readable contract

The preview palette is defined in:

```text
config/palettes-v1.2.json
```

It is deliberately separate from:

```text
config/palettes.json
```

so current V1.1 source remains the default build input until V1.2 acceptance is complete.

The preview contract records:

- `version: 1.2.0`;
- `lifecycle: development`;
- `stable_predecessor: 1.1.0`;
- Light, Dark, and Deep Dark variants;
- optical reference colors;
- interaction colors;
- Frost/material presentation tokens;
- GNOME Shell surface, hover, active, border, and shadow tokens.

## Optical references

The current preview uses these reference anchors:

| Role | Value |
| --- | --- |
| Frost White | `#F4F8FA` |
| Crystal White | `#FBFDFE` |
| Ice Blue | `#DCECF6` |
| Glacier Blue | `#8FC4E8` |
| Clear Sky Blue | `#68AEE0` |
| Cloud Gray | `#DCE3E8` |
| Slate Gray | `#7E8D99` |
| Cool Graphite | `#151C22` |
| Deep Graphite | `#0E1419` |
| Blue-Black | `#070C11` |

GoreeCloud's canonical platform blues remain identity colors:

- Primary Blue `#3B82F6`;
- Deep Blue `#174EA6`.

Those identity colors are not interchangeable with semantic success, warning, destructive, security, or privacy state.

## Appearance mapping

### Light

Light uses Frost White / Crystal White reading surfaces over a soft neutral canvas, graphite text, restrained Ice Blue environmental influence, and GoreeCloud Deep Blue for the primary interactive accent.

### Dark

Dark uses Cool Graphite as its environment, Deep Graphite for depth, Frost White text, and Clear Sky / Glacier blue interaction and reflection. It is tuned independently rather than produced by color inversion.

### Deep Dark

Deep Dark uses Blue-Black as the canvas, Deep Graphite and Cool Graphite structure, quiet Frost White text, Crystal/Ice edge light, and deliberately minimal atmospheric blue.

## Platform material boundary

V1.2's full optical material model cannot be reproduced exactly through GTK and GNOME Shell CSS. The Zorin adaptation therefore prioritizes:

1. hierarchy and readable contrast;
2. neutral/frosted surface relationships;
3. restrained compositor-supported translucency in GNOME Shell;
4. optical edge-light cues where reliable;
5. interaction-state clarity;
6. performance and native behavior over decorative imitation.

Unsupported backdrop/refraction behavior must not be faked at the expense of readability or native integration.

## Wallpaper relationship

The wallpaper collection is now intentionally decoupled from semantic UI accents.

Wallpaper source may use neutral environment tokens plus the canonical identity colors embedded in or associated with the relevant identity. It must not consume focus, selection, destructive, warning, or other semantic interaction tokens.

The target wallpaper character is:

- quiet environmental depth;
- soft cool light;
- low-frequency detail;
- subtle atmospheric color;
- generous calm regions suitable for Frosted UI;
- identity fidelity without oversized hero marks;
- no generic neon-technology or cyberpunk treatment.

The same source templates can be rendered against either the current V1.1 palette contract or the V1.2 preview environmental contract.

## Build the preview

Render the theme family without changing the default V1.1 build path:

```bash
python3 ./scripts/build.py \
  --palette-config config/palettes-v1.2.json \
  --output /tmp/goreecloud-zorin-v1.2/themes
```

Render all wallpaper variants against the V1.2 preview environment:

```bash
python3 ./scripts/build_wallpapers.py \
  --palette-config config/palettes-v1.2.json \
  --output /tmp/goreecloud-zorin-v1.2/wallpapers
```

Run the preview source gate:

```bash
python3 ./scripts/validate_v12_preview.py
```

The standard V1.1-compatible source validation remains:

```bash
./scripts/validate.sh --gtk
python3 ./scripts/validate_wallpapers.py
python3 ./scripts/validate_system_wallpapers.py
```

## Current acceptance gates

V1.2 must not be promoted merely because it builds. Acceptance requires evidence at the exact revision under review.

Required gates include:

- machine-readable contract validation;
- generated GTK/Shell source validation;
- wallpaper generation and canonical-identity preservation;
- representative rendered visual review in Light, Dark, and Deep Dark;
- keyboard/focus visibility;
- text legibility and 200%+ scaling checks;
- increased-contrast review where the platform supports it;
- reduced-transparency review where applicable;
- bright, dark, saturated, detailed, and no-wallpaper stress cases;
- GTK 3 native applications;
- GTK 4/libadwaita applications;
- GNOME Shell panel, Quick Settings, menus, notifications, overview, and dialogs;
- Zorin Appearance / Settings integration;
- performance and regression review;
- physical target-device review before release qualification.

## V1.1 → V1.2 migration sequence

1. Keep `config/palettes.json` and the current V1.1 default build path unchanged.
2. Develop V1.2 through `config/palettes-v1.2.json` and preview-only build commands.
3. Refine wallpaper and theme material mappings while preserving canonical identity artwork and native platform behavior.
4. Collect source-pinned target screenshots and interaction/accessibility evidence.
5. Resolve regressions without weakening semantic or identity contracts.
6. Only after V1.2 acceptance, promote the accepted V1.2 contract to the default palette/build path in one controlled migration.
7. Update lifecycle/version documentation and consumer target metadata in the same promotion change.
8. Keep rollback to the last accepted V1.1 revision available until post-promotion target verification is complete.

## Release boundary

A green CI run proves only the checks encoded in CI. It does not prove optical quality, accessibility completeness, target compatibility, or Stable qualification.

**Stable means verified, not assumed.**
