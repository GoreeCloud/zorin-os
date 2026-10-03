# GoreeCloud Glaze — Native Acceptance Checklist

Requirement Level: Mandatory

This checklist governs representative native validation for the Development theme. Source or CI success does not replace human/native evidence.

## 1. Preflight

Run:

    bash scripts/native-preflight.sh

Record the OS, GNOME, GTK 3, GTK 4, libadwaita, current GTK theme, User Themes availability, and whether both GoreeCloud variants are installed.

## 2. Install without applying

Run:

    bash scripts/install.sh

Verify both managed theme directories install under the user theme directory and that the active desktop theme does not change.

## 3. Light GTK review

Apply:

    bash scripts/install.sh --apply light

Review at minimum:

- Files / file chooser surfaces;
- Settings or another GTK 4 application;
- one GTK 3 application;
- title/header bars;
- menus and popovers;
- dialogs;
- text entry and selection;
- buttons, switches, check/radio controls;
- scrollbars and progress controls;
- keyboard focus;
- disabled controls;
- window inactive/backdrop states.

## 4. Dark GTK review

Apply:

    bash scripts/install.sh --apply dark

Repeat the same review and specifically confirm dark-preference requests do not fall back to the light semantic palette.

## 5. GNOME Shell and Zorin extensions

When the User Themes extension is available, apply the matching Shell variant and review:

- top/panel chrome;
- Zorin Taskbar;
- Zorin Menu;
- overview/app grid;
- search;
- popup menus;
- notifications;
- workspace switcher;
- app switcher;
- taskbar running indicators and badges;
- floating taskbar layouts if enabled.

Record any selector mismatch by exact Zorin/GNOME version.

## 6. Accessibility review

Review:

- keyboard-only navigation;
- focus visibility;
- text/background contrast;
- selected versus hovered state distinction;
- disabled-state readability;
- large text;
- relevant high-contrast behavior;
- Reduced Motion expectations;
- Reduced Transparency expectations;
- readable solid fallback surfaces where blur is unavailable.

Do not accept a state based only on color where the application itself is expected to supply label/icon semantics.

## 7. libadwaita gate

The Development theme intentionally does not ship the Zorin-supported GTK 4 `.libadwaita` opt-in marker.

Do not add the marker until representative libadwaita applications have been reviewed for widget geometry, color roles, focus, contrast, dialogs, navigation, and accessibility.

## 8. Rollback

To deactivate the installed managed theme files without deleting them irreversibly, run:

    bash scripts/uninstall.sh

Then restore the previously selected desktop theme through the normal Zorin Appearance / GNOME theme controls if needed.

## 9. Acceptance evidence

For each accepted candidate, record:

- exact repository revision;
- exact Development artifact identifier and checksum;
- Zorin OS version;
- GNOME version;
- GTK 3 / GTK 4 / libadwaita versions;
- light and dark screenshots;
- GTK 3 and GTK 4 application screenshots;
- Zorin Taskbar screenshot;
- Zorin Menu screenshot;
- focus-state screenshot;
- defects found and disposition;
- human/accessibility reviewer decision;
- Shell compatibility decision;
- libadwaita opt-in decision;
- downstream Glaze consumer decision.

The theme remains Development until all applicable mandatory gates close.
