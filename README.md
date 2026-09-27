# GoreeCloud for Zorin OS

This repository contains the Development-stage GoreeCloud desktop experience and workstation-specific applications for the verified Zorin OS 17.3 target environment.

The desktop project is **light-first**. `GoreeCloud-Zorin-Light` is the primary experience and the installer activates it together with the GoreeCloud icon theme, cursor theme, and primary light wallpaper. Dark and Deep Dark remain secondary compatibility variants.

## Project governance

Repository-level project authority is maintained in:

- [PROJECT-SPECIFICATIONS.md](PROJECT-SPECIFICATIONS.md) — current requirements, scope, architecture, security/privacy, platform, acceptance, and lifecycle obligations.
- [PROJECT-RECORD.md](PROJECT-RECORD.md) — significant desktop, Care, governance, migration, release, and acceptance history.

The release-scoped Care `apps/goreecloud-care/SPECIFICATIONS.md` remains historical Stable-0.1.0 evidence; it is not the current repository specification.

## Native applications

### GoreeCloud Care

GoreeCloud Care is developed in this repository under:

```text
apps/goreecloud-care/
```

It is a Development-stage local maintenance utility with scan/preview-first cache, thumbnail, stale user-owned temporary-file, Trash, APT-cache, disk/memory-status, and truthful Linux file-cache reclaim foundations. Routine user cleanup is unprivileged; permanent Trash deletion is separately confirmed; APT cache cleanup and file-cache reclaim cross a PolicyKit authorization boundary. It has no telemetry or network requirement in the current Development slice.

Care remains nonconformant/pre-release until its component Platform Contract and applicable Integral Platform System evidence, target Zorin OS 17.3 PolicyKit/runtime behavior, rendered/accessibility acceptance, package install/upgrade/rollback validation, and release gates are complete.

## Desktop assets

The repository currently provides:

- `GoreeCloud-Zorin-Light` — primary Applications/Shell theme;
- `GoreeCloud-Zorin-Dark` — secondary compatibility theme;
- `GoreeCloud-Zorin-DeepDark` — secondary compatibility theme;
- `GoreeCloud-Zorin` — light-first icon theme;
- `GoreeCloud-Zorin-Cursors` — Frost White + GoreeCloud Blue Xcursor theme;
- 24 identity-derived wallpaper source derivatives, with only 8 Light wallpapers exposed in Settings;
- recovery-backed replacement of the audited Zorin OS 17.3 stock wallpaper set without removing Zorin desktop packages.

The default installer now renders and composes the desktop against the **Glaze UI V1.2 Development** palette in `config/palettes-v1.2.json`. The V1.1 palette remains available as the stable predecessor/compatibility contract in `config/palettes.json`.

## Verified target

The installer supports the exact verified Zorin OS 17.3 theme package target. It fail-closes unless the local `zorin-desktop-themes` package and recorded GTK 3, GTK 4/libadwaita, and GNOME Shell base hashes match the tested environment.

The repository does not redistribute Zorin base-theme bytes. During installation, the composer reads and verifies the already-installed local Zorin theme files, copies them into temporary generated GoreeCloud themes, rewrites only the verified target GTK 4 selected/checked state blocks, and appends GoreeCloud semantic overrides using the selected V1.2 palette contract.

## Install the GoreeCloud desktop experience

```bash
./scripts/install.sh
```

The default install:

- generates and installs all three Applications/Shell variants under `~/.local/share/themes` using Glaze UI V1.2 Development;
- builds and installs `GoreeCloud-Zorin` under `~/.local/share/icons`;
- builds and installs `GoreeCloud-Zorin-Cursors` under `~/.local/share/icons`;
- activates `GoreeCloud-Zorin-Light` for Applications;
- activates `GoreeCloud-Zorin-Light` for Shell when the User Themes extension schema is available;
- activates the GoreeCloud icon theme;
- activates the GoreeCloud cursor theme;
- installs all 24 wallpaper source derivatives for compatibility/recovery;
- exposes only the 8 Light wallpapers in GNOME Settings;
- applies the primary Light wallpaper.

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

Build the icon theme without installing it:

```bash
python3 ./scripts/build_icons.py --output /tmp/goreecloud-icons
```

The generated icon theme is named:

```text
GoreeCloud-Zorin
```

It uses the light-first Glaze/GoreeCloud palette: Frost White, Crystal White, Ice Blue, Glacier Blue, GoreeCloud Primary Blue, Deep Blue, and graphite structure. The initial custom set covers core folders/places, home/desktop/trash, storage/devices, computer/phone/flash media, and `start-here`/GoreeCloud identity. Unoverridden icons inherit from the platform icon stack rather than disappearing.

The `start-here` and GoreeCloud identity icons preserve the synchronized canonical GoreeCloud mark already pinned by the repository branding authority.

## Cursor theme

Build the cursor theme without installing it:

```bash
python3 ./scripts/build_cursors.py --output /tmp/goreecloud-cursors
```

The generated Xcursor theme is named:

```text
GoreeCloud-Zorin-Cursors
```

It is generated with Python standard-library code and does not require `xcursorgen` at install time. The theme contains 24px, 32px, and 48px Xcursor image frames and custom Frost White / GoreeCloud Blue treatments for pointer, hand, text, crosshair, move, wait/progress, blocked, and resize cursor families, with common Xcursor aliases included.

## Wallpaper collection

The repository defines **24 3840×2160 SVG wallpaper source derivatives** across GoreeCloud, Glaze UI, Wardveil Security, and Privacy Shield.

The installed GNOME catalog is deliberately light-first: exactly **8 Light wallpapers are visible**, while the 16 Dark/Deep Dark compatibility derivatives remain installed as `deleted=true` catalog entries. This keeps source/recovery contracts complete without presenting dark wallpapers in Settings.

The wallpaper source is identity-derived rather than generic abstract artwork. Canonical branding authority is `GoreeCloud/goreecloud-branding-assets`; `config/wallpaper-identities.json` pins the authority commit, source path, synchronized copy, SHA-256, and viewBox used by generation.

Install or refresh wallpapers:

```bash
./scripts/wallpaper.sh install
```

Apply the default Light wallpaper:

```bash
./scripts/wallpaper.sh apply default
```

List the visible Light collection:

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

Run the complete desktop source validation set with:

```bash
./scripts/validate.sh --gtk
python3 ./scripts/validate_wallpapers.py
python3 ./scripts/validate_light_catalog.py
python3 ./scripts/validate_desktop_assets.py
python3 ./scripts/validate_v12_preview.py
python3 ./scripts/validate_system_wallpapers.py
```

Run the GoreeCloud Care Development validation/build with:

```bash
cd apps/goreecloud-care
sh ./scripts/validate.sh
sh ./scripts/build-deb.sh
```

The light-catalog gate verifies that all 24 compatibility entries remain valid while only the exact 8 Light wallpaper IDs are visible in the GNOME catalog.

CI keeps the existing desktop validation separate from Care's component-specific source/package and Platform Contract workflows so application work does not weaken or replace the theme acceptance surface.

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

Development / Draft. The primary desktop product direction is the light GoreeCloud experience, and GoreeCloud Care is a separate Development application component in the same Zorin OS repository. Source presence, installation success, green CI, or individual screenshots do not by themselves establish Stable qualification; real-device visual/accessibility and application-specific acceptance remain revision-specific.
