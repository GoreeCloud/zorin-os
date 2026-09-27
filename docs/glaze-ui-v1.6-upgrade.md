# GLAZE UI V1.6 Desktop Upgrade

## Scope

This record describes the current upgrade of the GoreeCloud Zorin OS theme from the historical V1.2 preview path to the consumer-eligible **GLAZE UI V1.6 / 1.6.0 Official Anchor**.

The repository remains Development. Shared Glaze UI lifecycle state does not replace exact-revision Zorin OS 17.3 acceptance.

## Upstream authority

- Repository: `GoreeCloud/glaze-ui`
- Release: `v1.6.0`
- Accepted release source: `a7180679ea851389e0f3004515f9a25f420e716d`
- Qualification source: `c7509c79256b04b0aa67cb9dd0737d7588e0ae4a`
- Downstream target: verified Zorin OS 17.3 theme package baseline

The current desktop palette in `config/palettes.json` is a Zorin-specific adaptation. It does not claim that downstream pigment values are new upstream Glaze tokens.

## Upgrade changes

The V1.6 migration:

1. makes `config/palettes.json` the single current install/build palette;
2. removes the V1.2 preview from default installer, wallpaper, light-catalog, and CI paths;
3. reconciles all 24 wallpaper catalog entries with the same current palette and source pin;
4. adds dedicated V1.6 Anchor/source-pin validation;
5. applies the stable material boundary: solid reading surfaces, bounded transient Glaze, and solid/raised fallback when backdrop behavior is unsupported;
6. introduces dedicated focus, success, warning, information, and destructive roles;
7. strengthens GTK focus to a 2 px ring with a 2 px offset where supported;
8. preserves the 32 px compact pointer floor and raises Shell quick controls to a 44 px coarse/touch-like target floor;
9. keeps semantic status separate from branding and prevents the theme from manufacturing privacy, security, protection, connectivity, or application truth;
10. retains exact-hash Zorin base composition, recovery backups, and package-safe stock-wallpaper diversion.

## Historical V1.2 material

`config/palettes-v1.2.json` and `docs/glaze-ui-v1.2-preview.md` remain for migration history and regression comparison only. They are not current installation or lifecycle authority.

## Source validation

The current source gate is:

```bash
python3 ./scripts/validate_v16_anchor.py
./scripts/validate.sh --gtk
python3 ./scripts/validate_wallpapers.py
python3 ./scripts/validate_light_catalog.py
python3 ./scripts/validate_desktop_assets.py
python3 ./scripts/validate_system_wallpapers.py
```

The V1.6 validator checks the exact upstream release/qualification pins, desktop material and target floors, semantic/focus contrast, Light/Dark/Deep Dark completeness, wallpaper/palette alignment, and successful generation of theme and wallpaper artifacts.

## Target acceptance still required

Before release promotion, the exact candidate still needs representative Zorin OS 17.3 review for:

- Light, Dark, and Deep Dark GTK 3 rendering;
- GTK 4/libadwaita applications including Files and Settings;
- GNOME Shell panel, search, overview/app grid, date/notification menu, and Quick Settings;
- keyboard focus visibility and navigation;
- increased contrast and reduced-transparency behavior where the platform exposes it;
- 200% text and layout expansion;
- bright, dark, saturated, and detailed wallpaper stress cases;
- Flatpak/Snap and application-specific theme boundaries;
- performance and regression behavior.

A green source/CI run is prequalification evidence only and does not establish Stable status.
