# GoreeCloud Themes for Zorin OS

This repository contains the Development-stage GoreeCloud desktop experience for the verified Zorin OS 17.3 target environment.

The project is **light-first**. `GoreeCloud-Zorin-Light` is the primary experience and the installer activates it together with the GoreeCloud icon theme, cursor theme, and primary light wallpaper. Dark and Deep Dark remain secondary compatibility variants.

The shared design-system source is consumer-eligible at GLAZE UI V1.6, but this repository remains **Development / Draft** until its own exact-revision Zorin OS 17.3 visual, accessibility, and runtime acceptance is complete. Upstream Anchor status is not treated as downstream release approval.

## Desktop assets

The repository currently provides:

- `GoreeCloud-Zorin-Light` — primary Applications/Shell theme;
- `GoreeCloud-Zorin-Dark` — secondary compatibility theme;
- `GoreeCloud-Zorin-DeepDark` — secondary compatibility theme;
- `GoreeCloud-Zorin` — light-first icon theme;
- `GoreeCloud-Zorin-Cursors` — neutral Frost White + Graphite Xcursor theme with restrained GoreeCloud Blue activity/action accents;
- 30 original Glaze UI wallpaper variants across Atmosphere, Terrain, Celestial, Architecture, and Digital categories;
- recovery-backed replacement of the audited Zorin OS 17.3 stock wallpaper set without removing Zorin desktop packages.

The default installer now renders and composes the desktop against the repository's **GLAZE UI V1.6 / 1.6.0 Official Anchor** desktop adaptation in `config/palettes.json`. The palette pins the accepted upstream release source `a7180679ea851389e0f3004515f9a25f420e716d`; the older `config/palettes-v1.2.json` file is retained only as historical migration provenance.

## Verified target

The installer supports the exact verified Zorin OS 17.3 theme package target. It fail-closes unless the local `zorin-desktop-themes` package and recorded GTK 3, GTK 4/libadwaita, and GNOME Shell base hashes match the tested environment.

The repository does not redistribute Zorin base-theme bytes. During installation, the composer reads and verifies the already-installed local Zorin theme files, copies them into temporary generated GoreeCloud themes, rewrites only the verified target GTK 4 selected/checked state blocks, and appends GoreeCloud semantic overrides using the selected V1.6 desktop palette contract.

## Install the GoreeCloud desktop experience

```bash
./scripts/install.sh
```

The default install:

- generates and installs all three Applications/Shell variants under `~/.local/share/themes` using the GLAZE UI V1.6 Official Anchor desktop adaptation;
- builds and installs `GoreeCloud-Zorin` under `~/.local/share/icons`;
- builds and installs `GoreeCloud-Zorin-Cursors` under `~/.local/share/icons`;
- activates `GoreeCloud-Zorin-Light` for Applications;
- activates `GoreeCloud-Zorin-Light` for Shell when the User Themes extension schema is available;
- activates the GoreeCloud icon theme;
- activates the GoreeCloud cursor theme;
- installs all 30 Glaze Originals wallpaper variants;
- exposes the complete light-first gallery in GNOME Settings: 10 Light, 10 Dark, then 10 Deep Dark;
- applies the primary Light Atmosphere — Cirrus wallpaper.

Existing GoreeCloud theme/icon/cursor directories are moved into timestamped recovery storage before replacement.

## Replace the stock Zorin wallpapers

To install the GoreeCloud desktop experience and replace the stock wallpaper gallery:

```bash
./scripts/install.sh --replace-stock
```

The target audit showed that directly purging the four Zorin wallpaper packages would also remove `zorin-os-artwork` and `zorin-os-desktop` and would pull in Ubuntu wallpaper packages. The project therefore **does not purge those packages**.

Instead, the replacement workflow keeps all Zorin packages installed and uses local `dpkg-divert` entries for the exact audited stock wallpaper images and GNOME background catalog files. Those files are moved under `/var/lib/goreecloud-zorin/stock-wallpaper-diversions`, outside normal GNOME wallpaper discovery paths. Package ownership remains intact, package upgrades continue to respect the diversions, and the GoreeCloud user catalog remains the visible replacement collection.

The workflow first verifies the target OS, exact wallpaper package versions, protected Zorin desktop/artwork package versions, exact package ownership for every audited file, and the complete GoreeCloud replacement catalog. It also records the unsafe `apt-get --simulate purge` result as diagnostic evidence but never executes that purge.

The same workflow is available independently:

```bash
./scripts/wallpaper.sh replace-stock plan
./scripts/wallpaper.sh replace-stock apply
./scripts/wallpaper.sh replace-stock status
./scripts/wallpaper.sh replace-stock restore
./scripts/wallpaper.sh replace-stock finalize
```

`restore` removes the local diversions and returns the stock files to their original paths. `finalize` discards the temporary transaction archive while leaving the package-safe diversions active; restore remains possible from the active diverted package files while the target package versions remain compatible.

## Icon theme

The icon contract is recorded in:

```text
config/desktop-assets.json
```

Build the deterministic base icon theme without installing it:

```bash
python3 ./scripts/build_icons.py --output /tmp/goreecloud-icons
```

The generated icon theme is named:

```text
GoreeCloud-Zorin
```

The base theme uses the light-first Glaze/GoreeCloud palette for first-party system assets and inherits unoverridden platform icons instead of allowing missing artwork.

### Third-party application normalization

The installer also performs a user-local third-party application-icon normalization pass:

```text
installed .desktop entries
        ↓
resolved original SVG/PNG identity
        ↓
Glaze optical safe-area scaling
        ↓
neutral Glaze presentation plate
        ↓
24 / 32 / 48 / 64 / scalable wrappers
```

The normalizer follows the inherited Glaze V1 icon-construction and identity contracts:

- preserve the external product's original identity;
- do not redraw, recolor into GoreeCloud branding, or replace third-party trademarks;
- use standard framing/padding to improve launcher-grid consistency;
- keep identity geometry inside the Glaze safe/primary optical zones;
- provide purpose-sized 24px, 32px, 48px, and 64px wrappers plus scalable presentation;
- leave GoreeCloud-prefixed first-party identities untouched;
- reject SVG sources containing scripts, foreign objects, or external/data/file resources;
- never modify third-party application packages or their `.desktop` files;
- fall back to inherited Zorin/Adwaita/hicolor artwork when a source icon cannot be resolved safely.

The presentation layer uses a restrained Frost/Crystal/Ice plate, soft Glacier outline, controlled highlight, and low-opacity Graphite depth. It deliberately normalizes visual weight without forcing every third-party mark into a new GoreeCloud symbol.

A normalization report is written into the installed icon theme at:

```text
~/.local/share/icons/GoreeCloud-Zorin/goreecloud-normalization-report.json
```

Install or update only the icon theme, without changing GTK/Shell themes, cursors, or the current wallpaper:

```bash
bash ./scripts/install_icons.sh
```

After installing new applications, refresh the existing icon wrappers with:

```bash
bash ./scripts/refresh_icons.sh
```

Preview what would be normalized without writing changes:

```bash
bash ./scripts/refresh_icons.sh --dry-run
```

Apps whose launcher uses an absolute icon-file path cannot be overridden through the freedesktop icon-theme lookup without rewriting the third-party launcher. GoreeCloud intentionally does not rewrite those launchers in this Development implementation; they remain inherited/original and are reported as skipped.

The core custom set still covers folders/places, home/desktop/trash, storage/devices, computer/phone/flash media, and `start-here`/GoreeCloud identity. The `start-here` and GoreeCloud identity icons preserve the synchronized canonical GoreeCloud mark already pinned by the repository branding authority.

See `docs/icon-normalization.md` for the detailed contract and target-review procedure.

## Cursor theme

Build the cursor theme without installing it:

```bash
python3 ./scripts/build_cursors.py --output /tmp/goreecloud-cursors
```

The generated Xcursor theme is named:

```text
GoreeCloud-Zorin-Cursors
```

The cursor is intentionally quieter than the rest of the desktop branding. Primary pointer, link hand, text, crosshair, move, and resize families use a familiar Frost White fill with a Graphite outline so they remain legible on both light and dark content. GoreeCloud Blue is reserved for activity/action accents such as progress spinners and the copy badge instead of outlining every cursor.

The generator uses only the Python standard library and does not require `xcursorgen` at install time. It renders a 24px, 32px, 48px, 64px, and 96px Xcursor size ladder with 4x supersampling and premultiplied-alpha downsampling. Wait and progress cursors use eight animation frames at a 55ms frame delay. Common Xcursor aliases and a dedicated copy cursor are included, while unoverridden cursor names inherit from Adwaita.

## Wallpaper collection

The repository defines **30 original 3840×2160 SVG wallpapers** designed with the Glaze UI V1.6 visual language. The catalog intentionally moves away from the earlier logo-centric set and treats wallpaper as environmental desktop art rather than a branding billboard.

The collection contains five categories with two distinct families each:

| Category | Families | Variants |
| --- | --- | ---: |
| Atmosphere | Cirrus, Halo | 6 |
| Terrain | Tundra, Strata | 6 |
| Celestial | Orbit, Aurora | 6 |
| Architecture | Atrium, Vault | 6 |
| Digital | Mesh, Current | 6 |
| **Total** | **10 families × Light/Dark/Deep Dark** | **30** |

Every family is rendered in Light, Dark, and Deep Dark. GNOME Settings remains **light-first, not light-only**: 10 Light wallpapers appear first, followed by 10 Dark and 10 Deep Dark wallpapers. Users may choose any wallpaper independently of the active desktop theme.

The source is pure repository-native vector artwork. It does not depend on stock imagery, external URLs, embedded raster data, or generated chat images. Shared Glaze identity comes from the V1.6 Frost/Crystal/Ice/Glacier/Graphite optical references, bounded translucency, restrained edge light, low-frequency composition, and generous quiet workspace regions. Semantic interaction colors such as focus, destructive, warning, success, and selection are prohibited as wallpaper presentation inputs.

Install or refresh wallpapers:

```bash
./scripts/wallpaper.sh install
```

Apply the default Light wallpaper:

```bash
./scripts/wallpaper.sh apply default
```

List the complete collection:

```bash
./scripts/wallpaper.sh list
```

Wallpaper files are installed under:

```text
~/.local/share/backgrounds/GoreeCloud-Zorin
```

The generated GNOME background catalog is installed at:

```text
~/.local/share/gnome-background-properties/goreecloud-zorin.xml
```

## Uninstall

```bash
./scripts/uninstall.sh
```

If the GoreeCloud GTK, Shell, icon, or cursor themes are currently selected, uninstall resets the corresponding GNOME setting to its distro default before moving the GoreeCloud files into timestamped recovery storage. Stock wallpaper replacement is managed separately through `wallpaper.sh replace-stock restore` when diversions are active.

## Validation

Run the complete source validation set with:

```bash
./scripts/validate.sh --gtk
python3 ./scripts/validate_wallpapers.py
python3 ./scripts/validate_light_catalog.py
python3 ./scripts/validate_desktop_assets.py
python3 ./scripts/validate_v16_anchor.py
python3 ./scripts/validate_system_wallpapers.py
```

The light-first catalog gate verifies that all 30 wallpapers are visible and ordered as 10 Light, 10 Dark, then 10 Deep Dark.

Icon validation now also exercises a synthetic third-party launcher/icon pair, verifies local-only normalized source references, verifies the 24/32/48/64/scalable wrapper ladder, and verifies that GoreeCloud-prefixed first-party identity is excluded from third-party normalization.

Cursor validation verifies the complete configured size ladder, animated-frame/delay contract, non-empty Xcursor payloads, and the neutral Frost/Graphite primary-pointer contract so the default pointer cannot regress to a blue-heavy treatment unnoticed.

CI runs ShellCheck plus wallpaper source/rendering, light-first catalog visibility, icon/cursor, V1.6 Anchor contract, stock-wallpaper safety, and generated GTK theme validation.

## Target diagnostics

Read-only target evidence tools include:

```bash
./scripts/diagnose.sh
python3 ./scripts/diagnose_gtk4_runtime.py
./scripts/diagnose_settings_css.sh
./scripts/diagnose_backgrounds.sh
```

The Development installer composes from the verified local Zorin 17.3 GTK 3, GTK 4/libadwaita, and GNOME Shell bases. Flatpak and Snap applications may retain bundled or sandboxed appearance behavior; browser chrome and web content can also use independent themes.

## Status

Development / Draft. The primary product direction is the light GoreeCloud experience. Source presence, installation success, green CI, or individual screenshots do not by themselves establish Stable qualification; real-device visual/accessibility acceptance remains revision-specific.
