# GoreeCloud Zorin — Glaze Application Icon Normalization

## Status

Development. This document describes the current third-party application-icon normalization layer for the GoreeCloud Zorin OS 17.3 desktop experience.

The implementation targets the current consumer-eligible **GLAZE UI V1.6 / 1.6.0 Official Anchor** and inherits the Glaze icon-construction and icon-identity contracts from the canonical `GoreeCloud/glaze-ui` repository.

## Purpose

The default Zorin/GNOME application grid mixes third-party icons with very different visual weights, canvas sizes, padding, geometry, and rendering styles. That inconsistency makes the launcher feel visually noisy even when every individual icon is technically correct.

The GoreeCloud normalization layer improves launcher-grid coherence without pretending third-party products are GoreeCloud products.

## Identity boundary

Third-party identities remain third-party identities.

The normalizer may apply:

- framing;
- optical padding;
- safe-area scaling;
- a neutral Glaze presentation plate;
- appearance-neutral depth/highlight treatment;
- optical-size adaptation.

It must not:

- redraw a third-party trademark as a GoreeCloud mark;
- replace an external identity with GoreeCloud family geometry;
- recolor an external product into protected GoreeCloud semantic colors merely for branding;
- edit a third-party application package;
- rewrite a third-party `.desktop` launcher in the current implementation.

GoreeCloud-prefixed first-party icons are deliberately excluded from the third-party normalizer so canonical first-party identity remains authoritative.

## Glaze construction mapping

The inherited Glaze master grid uses a 1024×1024 reference canvas.

Current normalization geometry:

| Role | Inset / size |
| --- | ---: |
| Presentation boundary | 64 px inset |
| Optical safe area | 128 px inset |
| Normalized identity content | 176 px inset |
| Core identity reference | 224 px inset |
| Presentation plate radius | 220 px |
| Runtime optical wrappers | 24 / 32 / 48 / 64 px + scalable |

The third-party source identity is therefore kept inside the Glaze primary region rather than stretched to fill the whole icon canvas.

## Presentation plate

The current Development plate uses:

- Crystal/Frost upper material;
- Ice lower material;
- restrained Glacier outline;
- internal white edge highlight;
- low-opacity Graphite depth.

The plate is intentionally neutral. It exists to equalize outer silhouette and visual weight, not to make every third-party icon look like a GoreeCloud first-party product.

## Runtime source discovery

`scripts/normalize_app_icons.py` scans installed application launchers and resolves theme-addressable icon names against common original-source locations such as:

- user and system hicolor themes;
- Flatpak exported hicolor icons;
- Snap desktop icon exports where theme-addressable;
- user/system pixmaps.

Supported source formats are SVG and PNG.

For SVG sources, the normalizer rejects:

- scripts;
- `foreignObject`;
- HTTP/HTTPS references;
- file references;
- data-URI references;
- protocol-relative external references.

A rejected or unresolved icon simply continues to inherit from the existing Zorin/Adwaita/hicolor stack.

## Generated structure

For every safely resolved third-party icon, the installed GoreeCloud theme receives wrappers under:

```text
scalable/apps/
24x24/apps/
32x32/apps/
48x48/apps/
64x64/apps/
```

The original source bytes are copied user-locally beneath the installed theme for wrapper reference. Application packages remain untouched.

The installed audit report is:

```text
~/.local/share/icons/GoreeCloud-Zorin/goreecloud-normalization-report.json
```

It records normalized icon names, unresolved icons, skipped entries, and source filenames without requiring mutation of the original applications.

## Install and refresh

The normalizer is run automatically by the full desktop installer:

```bash
./scripts/install.sh
```

For icon-only target testing or upgrades, use the recovery-backed icon installer:

```bash
bash ./scripts/install_icons.sh
```

That path replaces only `GoreeCloud-Zorin`, preserves the previous installed icon theme in timestamped recovery storage, rebuilds the cache, and re-emits the icon-theme setting. It does not change GTK/Shell themes, cursors, or wallpaper settings.

After installing additional applications:

```bash
bash ./scripts/refresh_icons.sh
```

Read-only preview:

```bash
bash ./scripts/refresh_icons.sh --dry-run
```

## Known limitation

Applications whose `.desktop` launcher uses an absolute icon-file path bypass ordinary icon-theme lookup. The current implementation reports those entries but does not shadow or rewrite their launchers. This preserves the minimum-change and third-party-integrity boundary.

If target evidence later shows that a small number of high-visibility absolute-path applications materially harm launcher quality, any future launcher-shadow mechanism must be separately designed, recovery-backed, provenance-aware, and validated before adoption.

## Validation

`scripts/validate_desktop_assets.py` requires:

- desktop-asset schema v2;
- normalization enabled;
- exact Glaze geometry references;
- 24/32/48/64 optical-size directories;
- no third-party package or launcher mutation;
- original-identity preservation;
- inherited fallback for unresolved icons;
- a synthetic third-party launcher successfully normalized;
- a synthetic GoreeCloud-prefixed launcher excluded from third-party normalization;
- wrapper source references to remain local to the generated icon theme.

## Target acceptance

Automated source validation is not visual acceptance.

Representative Zorin OS 17.3 review should verify:

- launcher-grid consistency before/after normalization;
- recognizable third-party branding;
- no clipped or excessively shrunken identities;
- compact-size legibility;
- app-menu and dock rendering;
- Files/Settings application icon rendering where applicable;
- light wallpaper stress;
- dark wallpaper stress;
- grayscale and Increased Contrast;
- first-party GoreeCloud icons remain canonical;
- unresolved/absolute-path icons fail gracefully rather than disappearing.

The icon system remains Development until exact-revision target screenshots establish acceptable launcher-grid quality.
