# GoreeCloud Zorin — Application Icon Presentation

## Status

Development / recovery-backed.

The first runtime third-party icon-wrapper implementation failed representative Zorin OS 17.3 visual acceptance on September 27, 2026. GNOME rendered the Glaze presentation plate while failing to render most wrapped third-party artwork, producing blank rounded-square icons in the launcher and dock.

That failed wrapper path is disabled and its active normalizer script has been removed.

## Verified recovery state

Target recovery restored the previous `GoreeCloud-Zorin` icon theme. A representative launcher screenshot then confirmed that recognizable original third-party artwork was visible again, including mixed native and third-party applications. The blank wrapper regression was no longer present.

## Current safe behavior

The `GoreeCloud-Zorin` icon theme continues to provide GoreeCloud/system icon overrides and inherits unoverridden artwork from:

```text
ZorinBlue → Adwaita → hicolor
```

Third-party application icon files are not rewritten, wrapped, masked, or recolored.

The supported icon-only recovery/install path is:

```bash
bash ./scripts/install_icons.sh
```

The runtime wrapper refresh path remains disabled:

```bash
bash ./scripts/refresh_icons.sh
```

That command only reports the disabled state and points back to the safe base icon installer.

## Replacement design: Shell application tiles

The replacement candidate improves visual consistency at the GNOME Shell application-tile layer rather than by replacing the icon resource.

The current source applies the Glaze treatment to:

```text
.overview-tile
.grid-search-result
```

The original application artwork remains untouched inside the tile.

Current tile contract:

| Property | Value |
| --- | ---: |
| Padding | 8 px |
| Internal spacing | 6 px |
| Corner radius | 16 px |
| Border | 1 px Glaze Shell border |
| Base surface | Glaze Shell elevated surface |
| Focus ring | minimum 2 px |
| Hover | Glaze hover surface + accent-soft border |
| Active | Glaze active surface |

This follows the existing Zorin Shell styling model, which already treats overview/search application items as rounded presentation tiles. GoreeCloud changes the shared tile rhythm, not the third-party identity asset.

## Target-only launcher update

For representative target review, install only the generated GoreeCloud Shell presentation:

```bash
bash ./scripts/install_launcher_presentation.sh
```

That installer:

- rebuilds the three GoreeCloud Shell variants from the canonical V1.6 palette;
- composes them against the exact verified local Zorin OS 17.3 Shell base;
- replaces only installed `gnome-shell` directories;
- stores the previous Shell directories in timestamped recovery storage;
- re-emits the currently selected GoreeCloud User Theme when necessary;
- does not change GTK application theme, icon theme, cursor theme, or wallpaper settings;
- does not modify any third-party application icon or launcher.

## Failure record

The failed Development implementation attempted to discover installed third-party icon sources and create Glaze SVG wrappers at multiple optical sizes. Synthetic CI validated the XML/resource structure, but real-device GNOME rendering showed that this was not sufficient runtime evidence.

The incident establishes an explicit rule for this downstream theme:

> A third-party icon presentation feature must never replace a directly renderable icon with a wrapper unless representative target evidence proves the complete original artwork renders inside that wrapper.

## Validation

`scripts/validate_desktop_assets.py` currently enforces:

- runtime third-party icon wrappers remain disabled;
- no third-party application package or `.desktop` mutation;
- original third-party identity preservation;
- inherited fallback for unoverridden application icons;
- safe Shell tile presentation is enabled;
- tile presentation targets only `.overview-tile` and `.grid-search-result`;
- 8px padding, 6px spacing, 16px radius, and at least a 2px focus ring;
- the required Glaze Shell surface/border/focus fragments remain in the generated Shell template;
- disabled wrapper optical directories are not advertised by the icon theme.

## Target acceptance

The launcher-tile candidate must be reviewed on the representative Zorin OS 17.3 target with screenshots showing:

- the application menu with several full rows;
- selected/focused application state;
- mixed icon families such as browser, creative, utility, GNOME, Flatpak/Snap, and GoreeCloud apps;
- the dock/taskbar;
- light and dark wallpaper conditions.

Acceptance requires that the tiles make the launcher feel more ordered **without** obscuring, shrinking, clipping, recoloring, or replacing the original application icons.

The PR remains Draft until that visual review passes.
