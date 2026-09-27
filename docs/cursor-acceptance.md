# GoreeCloud Zorin Cursor Acceptance

Status: Development / target-device acceptance aid.

This checklist is for GoreeCloud cursor design revision 2 on the verified Zorin OS 17.3 target. It does not promote the cursor theme or desktop theme, and the shared GLAZE UI V1.6 Official Anchor does not substitute for downstream Zorin acceptance.

## Preconditions

Install the current `feat/zorin-glaze-theme` candidate and verify that the revisioned runtime identity is active:

```bash
python3 ./scripts/preview_cursors.py --check
```

The expected active cursor runtime is `GoreeCloud-Zorin-Cursors-r2` for design revision 2. The check fails closed if the active GNOME setting differs or if any acceptance cursor alias is missing from the installed runtime theme.

## Interactive review

Launch the light-first acceptance surface:

```bash
python3 ./scripts/preview_cursors.py
```

The window presents the same cursor families on explicit Light and Dark GoreeCloud surfaces. Hover each tile to load the requested cursor through GDK. Click the `⊕` target in a tile to get an approximate hotspot click offset from the target center.

Review these states separately:

- default pointer;
- link hand;
- text I-beam;
- crosshair;
- move;
- horizontal and vertical resize;
- both diagonal resize directions;
- wait animation;
- progress animation;
- copy action;
- forbidden/not-allowed;
- Light-background legibility;
- Dark-background legibility;
- practical hotspot behavior.

A good result means the cursor is immediately recognizable, visually balanced at the active desktop cursor size, legible without a blue-heavy outline, and aligned closely enough that the visible interaction point matches the actual click location. Wait and Progress must visibly animate rather than appearing as a static frame.

## Acceptance boundary

The default pointer has already received positive target feedback after the revisioned runtime identity was activated. That acceptance does not automatically cover the remaining cursor states. Record only states that were directly exercised on the target device.
