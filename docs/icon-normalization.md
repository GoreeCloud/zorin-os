# GoreeCloud Zorin — Application Icon Normalization

## Status

Development / rollback-safe.

The first runtime third-party icon-wrapper implementation failed representative Zorin OS 17.3 visual acceptance on September 27, 2026. GNOME rendered the Glaze presentation plate but failed to render most wrapped third-party application artwork inside it, producing blank rounded-square icons in the launcher and dock.

That failed runtime path is disabled in the current source.

## Current safe behavior

The `GoreeCloud-Zorin` icon theme continues to provide GoreeCloud/system icon overrides and inherits the rest from:

```text
ZorinBlue → Adwaita → hicolor
```

Third-party application icons therefore remain their original renderable artwork unless an explicit first-party-safe override already exists.

The installers do not:

- generate third-party runtime wrapper icons;
- modify third-party application packages;
- rewrite third-party `.desktop` files;
- replace external product identities with GoreeCloud marks.

Use the icon-only installer to restore or refresh the safe base theme:

```bash
bash ./scripts/install_icons.sh
```

The refresh helper intentionally does not regenerate wrappers:

```bash
bash ./scripts/refresh_icons.sh
```

It reports that runtime normalization is disabled and points back to the safe base-theme installer.

## Failure record

The failed Development implementation attempted to:

- discover installed third-party icon sources;
- copy those sources beneath the GoreeCloud icon theme;
- generate Glaze plate wrappers at scalable and 24/32/48/64 optical sizes;
- reference the copied original artwork from inside each wrapper.

Source validation and synthetic CI fixtures passed, but real Zorin OS 17.3 visual evidence showed that the wrapper resource path was not reliably rendered by the actual GNOME launcher/icon stack.

The failure demonstrates that structural XML validity and source existence are insufficient acceptance evidence for runtime icon rendering.

## Replacement requirements

The next normalization design must preserve the application's directly renderable original icon and improve consistency at the presentation/layout layer rather than by replacing the icon resource with a wrapper that depends on nested resource loading.

A future replacement should satisfy all of the following:

- original third-party identity remains recognizable and authoritative;
- no blank placeholder or plate-only state is possible;
- no mutation of third-party application packages;
- no launcher rewriting unless separately designed, recovery-backed, and explicitly validated;
- consistent optical padding and visual weight where the target Shell/launcher safely supports it;
- clean fallback to inherited artwork when a presentation treatment cannot be applied;
- representative real-device acceptance in the Zorin app grid and dock;
- light and dark wallpaper stress testing;
- compact-size legibility;
- accessibility review;
- no Stable qualification based only on synthetic CI.

## Validation

`scripts/validate_desktop_assets.py` currently enforces the rollback-safe state:

- runtime third-party wrappers are disabled;
- third-party packages and launchers are not modified;
- original identity preservation remains required;
- unresolved/unoverridden applications continue through inherited icon themes;
- the GoreeCloud first-party/base icon theme and cursor contracts remain validated.

The previous normalizer source may remain temporarily in the repository as Development provenance, but no supported installer or refresh path may invoke it while the failure is unresolved.

## Target acceptance

The next candidate must be reviewed on the representative Zorin OS 17.3 target with screenshots showing:

- launcher grid;
- dock/taskbar;
- a mix of native, Flatpak, Snap, and third-party application icons;
- first-party GoreeCloud icons;
- light and dark desktop backgrounds.

The icon-normalization work remains open until those screenshots show consistent organization without sacrificing original icon rendering.
