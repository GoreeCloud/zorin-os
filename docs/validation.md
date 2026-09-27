# Validation and Acceptance

## Current verified state

The repository validation tooling verifies:

- palette JSON structure and unique theme identifiers;
- deterministic generation of all three GoreeCloud override variants;
- presence of `index.theme`, the GTK 2 discovery compatibility shim, GTK 3 CSS, GTK 4 CSS, the Zorin `.libadwaita` opt-in marker, and GNOME Shell CSS in standalone generated output;
- the GTK 2 compatibility shim inherits the system Adwaita GTK 2 theme;
- balanced GTK 3/GTK 4/Shell stylesheet braces and no unresolved template tokens;
- a GTK 3 Adwaita compatibility-base import in each standalone generated application theme;
- GTK 3 legacy symbolic color mappings used by application-provided CSS such as Nautilus 42.6;
- an exact Nautilus 42.6 `.nautilus-window .sidebar-row:selected` override in GTK 3;
- GTK 3 generic `row:selected` mapping to the current variant's Glaze selection token;
- GTK 3 checked-switch image-state and slider mappings to the current variant's Glaze accent/on-accent tokens;
- GTK 4/libadwaita color-role mappings, exact `navigation-sidebar` selected/activatable states, checked-switch state coverage, and an empty marker at exactly `gtk-4.0/.libadwaita`;
- GTK 4 generated selected-row and checked-switch image layers map to the current GoreeCloud variant's selection/accent tokens rather than retaining Zorin's pale-cyan image fills;
- shell-script syntax, Python compilation, and expected executable bits for executable repository tools, including the focused runtime trace helper and Settings CSS/GResource diagnostic;
- presence of the exact Zorin OS 17.3 target package/version and pinned GTK 3, GTK 4, and GNOME Shell base stylesheet size/SHA-256 evidence in the composition implementation;
- source evidence that target installation copies the verified local Zorin GTK 3 base and removes the standalone GTK 3 Adwaita import before appending GoreeCloud overrides;
- a basic reusable-secret scan;
- optional GTK 3 and standalone GTK 4/libadwaita override smoke-loading under a virtual display.

These checks support **source validation** only. Stock Ubuntu CI does not reproduce the verified Zorin OS 17.3 desktop session or target application stack.

## Target-device evidence so far

The Zorin OS 17.3 target laptop has provided the following direct evidence during this Development cycle:

- all three theme variants install successfully under `~/.local/share/themes` and remain discoverable in Zorin Appearance;
- the GTK 2 compatibility shim resolved Applications-theme enumeration;
- `GoreeCloud-Zorin-Dark` is selectable for both **Applications** and **Shell**;
- the Zorin Appearance **Zorin / Other** stack-switcher contrast repair is visually verified;
- exact-base composition is installed and provenance-verified for GTK 3, GTK 4, and GNOME Shell;
- after a full Shell reload, Quick Settings checked toggles use the GoreeCloud Mineral Teal family rather than the original bright Zorin cyan;
- the date/notification menu uses coherent dark cards and readable calendar/date text;
- the Zorin application-menu selected tile is readable and its tooltip is readable; the empty search placeholder still needs a dedicated contrast check;
- representative GNOME overview/search rendering is coherent dark with a visible teal focus treatment;
- **Files / Nautilus 42.6** renders the intended Dark canvas `#101A20`, Dark surface `#18252B`, and selected Home row `#174F52`;
- a fresh **Settings → Search** target retest after the requested install/restart sequence verifies that enabled switch tracks now render the intended Mineral Teal `#1C8A8D`; this closes the prior Dark Settings checked-switch palette defect;
- the same fresh Settings screenshot shows the selected **Search** navigation row still renders exact Zorin pale cyan `#BDE6FB` instead of the intended Dark selection `#174F52`; the selected-row state is now the only remaining Settings palette blocker from this checkpoint;
- the installed GoreeCloud Dark GTK 4 files do contain the intended `#174F52` selected-row and `#1C8A8D` checked-switch mappings, but a complete focused target trace of `gnome-control-center search` did not open any active-theme GTK 4 path or `.libadwaita` file;
- the same Settings PID did open `/home/slickkredd/.local/share/themes/GoreeCloud-Zorin-Dark/gtk-3.0/gtk.css`;
- direct package/linkage evidence identifies Settings as `gnome-control-center` `1:41.7-0ubuntu0.22.04.9+zorin1`, directly linked to `libhandy-1.so.0`, `libgtk-3.so.0`, and `libgdk-3.so.0`, with no direct GTK 4 or libadwaita dependency;
- therefore the remaining Settings selected-row defect is classified as a **GTK 3/libhandy state issue**, not a GTK 4/libadwaita provider-loading issue;
- the verified ZorinBlue-Dark GTK 3 base contains generic `row:selected { background-color: #bde6fb; }` behavior and `switch:checked { background-color: #bde6fb; background: image(#bde6fb); }`, which directly explained the two earlier Settings colors;
- current Development maps those GTK 3 state mechanisms to GoreeCloud Glaze semantic tokens. Target rendering now proves the switch mapping is effective but the generic row mapping is not sufficient to displace the selected Search row;
- because the appended theme override successfully controls the switch while the selected Search row remains pale cyan, the next evidence step is a bounded, read-only inspection of installed GNOME Control Center/libhandy CSS and embedded GResources before any more specific styling rule is added;
- Firefox demonstrates that browser-provided/bundled chrome and content styling may remain visually independent from the GTK theme and therefore must not be treated as GTK acceptance evidence.

This is **partial Dark-mode acceptance evidence**, not complete visual or accessibility acceptance.

## Captured Zorin OS 17.3 implementation evidence

The target diagnostics establish this environment:

- Zorin OS 17.3 (`VERSION_ID=17`);
- Wayland session, `zorin:GNOME`, GNOME Shell 43.9;
- Nautilus 42.6 (`1:42.6-0ubuntu2`);
- GNOME Control Center / Settings `1:41.7-0ubuntu0.22.04.9+zorin1` using GTK 3 + libhandy;
- `zorin-desktop-themes` 4.2.2;
- `zorin-appearance` 5.3.8;
- `libadwaita-1-0` `1.3.3-0ubuntu0.23.04.1+zorin2` is installed for other applications, but the traced Settings executable does not directly link it;
- `gnome-shell` `43.9-0+deb12u2+zorin3`;
- GTK theme `GoreeCloud-Zorin-Dark`, color scheme `prefer-dark`, Shell user theme `GoreeCloud-Zorin-Dark`.

The exact locally installed Zorin base stylesheet evidence is:

| Base file | Bytes | SHA-256 |
| --- | ---: | --- |
| `ZorinBlue-Light/gtk-3.0/gtk.css` | 215389 | `bc06ff2fac92e56951b8f4141b8324acc1e38db783ec3a0b3cf438e8c87d9fe6` |
| `ZorinBlue-Light/gtk-4.0/gtk.css` | 196060 | `b29cfbaa713955b14517798e2c15a67184136d9913944c1d0cf22fce0d1b3e0c` |
| `ZorinBlue-Light/gtk-4.0/gtk-dark.css` | 195469 | `90ffa76c872443d1549f09c814be8c22d68169a0dfb19e0508339e3613add77d` |
| `ZorinBlue-Light/gnome-shell/gnome-shell.css` | 110634 | `3d94563d7c680be4ac0632b95bb0c205954377488c774a653d8655dbc2ca0823` |
| `ZorinBlue-Dark/gtk-3.0/gtk.css` | 214797 | `71e9d93ad1e58f75e52bb7b724fa38409961368b5d9edda4c3b921fac6e44604` |
| `ZorinBlue-Dark/gtk-4.0/gtk.css` | 195469 | `90ffa76c872443d1549f09c814be8c22d68169a0dfb19e0508339e3613add77d` |
| `ZorinBlue-Dark/gtk-4.0/gtk-dark.css` | 195469 | `90ffa76c872443d1549f09c814be8c22d68169a0dfb19e0508339e3613add77d` |
| `ZorinBlue-Dark/gnome-shell/gnome-shell.css` | 111171 | `e36202095055bda8de6f225227a91911623775aa0896c24b8568c0d52982f8d7` |

This evidence confirms that the target GTK 3, GTK 4, and Shell implementations are substantial Zorin-specific bases rather than tiny semantic overlays. Current upstream Zorin theme source must not be substituted for the installed 17.3 package without verification; public source is used only to understand selector/property mechanisms that are then tied back to target-device evidence.

## Development base-composition architecture

The Development installer uses an evidence-bound composition step instead of attempting to replace the Zorin compatibility foundation:

1. `scripts/build.py` generates standalone GoreeCloud GTK 3, GTK 4, and Shell semantic override stylesheets.
2. `scripts/compose_zorin_base.py` requires `zorin-desktop-themes` 4.2.2 and verifies the recorded ZorinBlue Light/Dark GTK 3, GTK 4, and Shell base file sizes/SHA-256 hashes before making a composed theme.
3. Light uses the verified local `ZorinBlue-Light` base. Dark and Deep Dark use the verified local `ZorinBlue-Dark` base.
4. The compositor copies the complete local GTK 3, GTK 4, and GNOME Shell base directories, including supporting assets, into temporary generated theme folders.
5. The standalone GTK 3 Adwaita import is removed only for target-base composition, preventing a second compatibility base from being imported after the verified Zorin GTK 3 foundation.
6. GoreeCloud GLAZE UI V1.6 desktop semantic overrides are appended after each verified local base.
7. GTK 3 generic selected rows and checked-switch image/slider states are explicitly remapped because the verified Settings executable consumes GTK 3 and the verified Zorin base hard-codes those pale-cyan states there. The switch remap is target-verified; the generic selected-row remap remains insufficient for Settings Search and is not accepted as the final row fix.
8. `gtk-dark.css` is composed to the explicit selected GoreeCloud variant where applicable so a separate dark-preference path does not silently replace the selected Applications variant during this acceptance cycle.
9. The empty `.libadwaita` opt-in marker is restored after GTK 4 composition for applications that actually use the GTK 4/libadwaita path.
10. `goreecloud-base.json` records local base provenance; the installed package copyright record is copied as `ZORIN_BASE_COPYRIGHT` when available.
11. The GoreeCloud repository does not redistribute Zorin base-theme bytes; composition copies them locally from the already-installed Zorin package.
12. The installer performs all verification and temporary composition **before** moving or replacing an existing installed GoreeCloud theme. A package/hash mismatch therefore fails closed without disturbing the current installed theme.
13. `scripts/diagnose_settings_css.sh` is a read-only target helper used to locate installed GNOME Control Center/libhandy standalone CSS or embedded GResource state rules before another selected-row selector is attempted.

The exact-base architecture is target-verified for the captured Dark Files surfaces, Files selected-sidebar state, and Settings checked-switch state. The Settings selected Search row remains unresolved.

## Required target-device acceptance

Before this theme is treated as release-ready or Stable, validate it on the intended Zorin OS 17.3 laptop.

1. Pull the current Development branch and run `./scripts/install.sh` after each source candidate that changes application or Shell styling.
2. Confirm the installer reports successful composition against verified `ZorinBlue-Light` / `ZorinBlue-Dark` GTK 3, GTK 4, and Shell bases before installation.
3. Confirm `goreecloud-base.json` records `gtk3_css`, `gtk_css`, and `shell_css` evidence for the selected base.
4. Preserve the already-verified Files Dark canvas/sidebar and `#174F52` selected-sidebar treatment when testing later candidates.
5. Preserve the now-verified Dark Settings checked-switch track at Mineral Teal `#1C8A8D`; resolve and re-test the selected **Search** navigation row, which still renders `#BDE6FB` instead of Dark selection `#174F52`.
6. Before another Settings selected-row styling change, run `./scripts/diagnose_settings_css.sh` and inspect the bounded installed GNOME Control Center/libhandy CSS/GResource evidence for a more specific or higher-priority selected-row contract.
7. Close and reopen **Zorin Appearance → Themes → Other** and confirm all three variants remain available under Applications and Shell.
8. Test matching Light, Dark, and Deep Dark Application + Shell combinations.
9. For GTK 4/libadwaita acceptance, confirm at least one separate native libadwaita application adopts expected GoreeCloud canvas, surface, sidebar, selected-row, headerbar, popover, button, field, and focus colors without clipping or broken controls.
10. Install/run `libadwaita-1-examples` / `adwaita-1-demo` on the target laptop when available and inspect representative controls before release qualification.
11. Inspect Terminal, dialogs, file pickers, menus, context menus, search fields, tabs, buttons, switches, checkboxes, scrollbars, progress bars, tooltips, and notifications.
12. After each Shell-theme update, switch the Shell theme away and back or log out and back in, then inspect the top panel, GNOME overview/dash when applicable, Zorin application menu/app grid, search, Quick Settings, system menu, notification/date menu, and modal dialogs.
13. Re-check the Zorin application-menu search placeholder for sufficient contrast.
14. Verify keyboard navigation and clearly visible focus states.
15. Verify text remains readable at normal and increased text scaling.
16. Check selected, hover, active, disabled, destructive, and suggested-action states for adequate distinction.
17. Confirm no clipping, unreadable text, invisible icons, broken separators, or unusable controls.
18. Verify the theme can be switched away from cleanly and that `./scripts/uninstall.sh` preserves a recovery copy instead of deleting installed theme folders.
19. Check representative Flatpak and Snap applications and document which ones retain bundled styling.

## Acceptance boundary

A successful build, pull request, CI run, theme-discovery fix, base hash match, local composition, GTK 3 smoke-load, GTK 4 smoke-load, presence of the `.libadwaita` marker, runtime trace, toolkit-linkage result, or an individual visually improved state does not prove the final desktop experience. Target-device rendering and accessibility acceptance are still required.
