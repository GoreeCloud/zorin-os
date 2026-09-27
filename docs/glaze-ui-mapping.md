# GLAZE UI V1.6 Mapping for Zorin OS

## Status

This document records the GoreeCloud Zorin OS desktop adaptation of **GLAZE UI V1.6 / 1.6.0 Official Anchor**.

Upstream authority is `GoreeCloud/glaze-ui`. This repository pins the accepted V1.6 release source at `a7180679ea851389e0f3004515f9a25f420e716d` and its qualification source at `c7509c79256b04b0aa67cb9dd0737d7588e0ae4a`.

This is a downstream platform adaptation. It does not transfer upstream acceptance to the Zorin theme. The theme remains Development until its own exact-revision target acceptance is complete.

## Governing desktop rule

The V1.6 material rule is applied conservatively:

> Solid where users read or make explicit critical decisions. Glazed where users interact with transient navigation, command, search, control, or feedback chrome.

GTK and GNOME Shell cannot reproduce every Glaze optical behavior. Unsupported backdrop effects therefore fail toward solid or raised surfaces instead of becoming low-contrast transparency.

## Surface and material mapping

| Glaze UI role | Zorin / GTK / GNOME Shell mapping |
| --- | --- |
| Canvas | application/window background and lowest desktop content layer |
| Solid | reading surfaces, forms, dense lists, settings content, explanatory text |
| Raised | cards, sidebars, inspectors, floating but content-bearing panels |
| Functional Glass | bounded Shell panel, search, quick controls, menus, transient navigation chrome |
| Overlay | dialogs, popovers, sheets, OSDs, high-authority transient surfaces |
| Clear Glass | not used as a default content material |
| Unsupported backdrop | solid or raised neutral fallback |

The adaptation avoids nested backdrop stacks and intentionally keeps Shell translucency high-opacity because GNOME Shell CSS cannot guarantee the same bounded blur semantics as the shared Glaze runtime.

## Color and semantic-state mapping

The desktop palette uses Frost White, Ice Blue, GoreeCloud Blue, and Cool Graphite as its product/environment identity. Pigment values in `config/palettes.json` are downstream Zorin implementation values; they are not promoted as new upstream Glaze tokens.

Interaction and state roles are separate:

- `accent` is ordinary interaction emphasis;
- `focus` is explicit keyboard/accessibility focus and remains visibly distinct from hover;
- `selection` is a stable selected-state surface;
- `success`, `warning`, `information`, and `destructive` have dedicated colors;
- the theme does not infer privacy, security, protection, connectivity, or application state;
- semantic meaning must not rely on color alone.

GTK 4/libadwaita named semantic colors are mapped from these roles where the toolkit exposes them. GTK 3 retains compatible symbolic aliases without overriding application truth.

## Geometry and target floors

The desktop adaptation keeps the established Glaze spacing/radius hierarchy while respecting native widget constraints:

- compact controls use a minimum 32 px pointer target;
- quick settings and coarse/touch-like Shell controls use a 44 px minimum target;
- common controls use approximately 16 px radii;
- menus/tooltips use quieter compact geometry;
- major dialogs, dash surfaces, and quick-settings containers use approximately 24 px radii;
- switches, scroll thumbs, and progress tracks may use capsule geometry.

Density changes must not reduce the applicable target floor.

## Focus and interaction states

GLAZE UI V1.6 requires focus to remain visible across materials, reduced motion, reduced transparency, and constrained-performance presentation.

The Zorin mapping therefore uses:

- a dedicated `focus` token rather than hover styling;
- a minimum 2 px GTK focus outline with a 2 px offset where GTK supports it;
- a strong 2 px structural focus ring in GNOME Shell, whose St CSS model does not offer the same outline-offset behavior;
- separate hover, focus, pressed/active, selected, disabled, and destructive presentation where the platform exposes those states.

Hover is never the only visible interaction path.

## Appearance modes

The family exposes:

- `GoreeCloud-Zorin-Light` — primary light-first experience;
- `GoreeCloud-Zorin-Dark` — secondary dark compatibility experience;
- `GoreeCloud-Zorin-DeepDark` — secondary deep-dark compatibility experience.

Each mode uses the same semantic role structure and accessibility floors.

## GTK 3

GTK 3 remains based on the exact locally installed, hash-verified Zorin OS 17.3 theme. GoreeCloud overrides are appended only after the verified base is copied into the generated theme.

The mapping covers symbolic GTK colors, header bars, buttons, fields, selections, switches, menus, sidebars, Files/Settings target selectors, focus, progress, scrollbars, and common geometry.

## GTK 4 / libadwaita

Zorin OS 17+ requires the generated empty `gtk-4.0/.libadwaita` marker before native libadwaita applications can load the third-party theme path used by this project.

The GTK 4 mapping covers window/view/header/sidebar/card/dialog/popover roles, accent and semantic colors, selected navigation rows, checked controls, focus, progress, scrollbars, and Zorin-target Files/Settings selectors.

The composer rewrites only the exact selected-row and checked-switch blocks in the hash-verified Zorin 17.3 GTK 4 base before appending GoreeCloud overrides.

## GNOME Shell

Shell surfaces use bounded, high-opacity neutral Glaze presentation for the panel, menus, dash, search, notifications, date/calendar surfaces, quick settings, and icon buttons.

Quick settings use 44 px minimum targets, dedicated focus treatment, neutral elevated surfaces, and selection/accent roles without reviving Zorin's inherited cyan gradients.

## Accessibility and degradation

The source-level adaptation enforces or records:

- strong primary text contrast;
- minimum muted-text and foreground/background contrast checks;
- focus contrast checks;
- solid/raised fallback for unsupported or reduced transparency;
- no decorative motion dependency;
- no color-only status contract;
- preserved target floors under density changes;
- protected content/action/focus/hierarchy semantics when effects are reduced.

Actual keyboard behavior, high-contrast behavior, reduced-transparency behavior, 200% text legibility, GTK 4/libadwaita rendering, Shell rendering, and representative wallpaper stress cases still require target acceptance on the exact candidate revision.

## Platform limits

GTK, libadwaita, and GNOME Shell CSS do not implement the complete Glaze optical engine, connected transformations, runtime context adaptation, or all shared material behaviors. This theme therefore prioritizes semantic hierarchy, readability, geometry, focus, state clarity, and conservative material fallbacks rather than simulating unsupported effects.

GTK 2 remains a discovery compatibility shim. Flatpak/Snap applications, browser chrome, and applications with bundled CSS may retain independent styling.
