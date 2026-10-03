# GoreeCloud for Zorin OS — Planned Features

**Status:** Active repository roadmap control  
**As of:** 2026-10-03  
**Canonical repository:** `GoreeCloud/zorin-os`

## Purpose

This file records current planned and gated work for repository-owned Zorin OS themes and GoreeCloud Care without replacing implementation evidence, release gates, or GoreeCloud Tasks Management.

## Theme roadmap

| ID | Feature / obligation | Priority | Current state |
| --- | --- | --- | --- |
| THEME-002 | Perform representative Zorin OS native rendering and interaction validation for the exact GoreeCloud Glaze theme candidate, including GTK 3, GTK 4, window chrome, menus, dialogs, navigation, focus, light/dark presentation, and common Zorin applications. | High | Planned / acceptance gated |
| THEME-003 | Perform human visual and accessibility review, including keyboard focus visibility, contrast, Reduced Motion/Reduced Transparency behavior where supported, readable fallback surfaces, large text, and common high-contrast behavior. | High | Planned / acceptance gated |
| THEME-004 | Verify GNOME Shell variant compatibility on supported Zorin/GNOME generations with a compatible User Themes extension, and document any selectors that require version-specific adaptation. | High | Planned / acceptance gated |
| THEME-005 | Define and publish the accepted distribution/package boundary only after exact-candidate native acceptance is complete; do not represent the Development source as Stable before that gate closes. | Medium | Blocked until acceptance closes |

## GoreeCloud Care roadmap

**Authoritative project record:** Project Specification — Care  
**Component path:** `apps/goreecloud-care/`

| ID | Feature / obligation | Priority | Current state |
| --- | --- | --- | --- |
| CARE-001 | Create and qualify the separate Care Stable source/package identity without rewriting accepted Release Candidate history. | High | Planned / gated |
| CARE-002 | Produce immutable exact Stable package, checksum, cross-environment, installed-lifecycle, and provenance evidence. | High | Planned / gated |
| CARE-003 | Rebind or refresh Privacy Shield, Wardveil Security, Everkeep, representative-target, and Glaze evidence when their exact-source freshness rules require it. | High | Planned / gated |
| CARE-004 | Perform explicit Stable promotion only after every applicable exact Stable gate passes. | High | Blocked until gates close |

## Repository-native maintenance

Google Drive roadmap synchronization is retired. Maintain this file from authoritative repository/project evidence and applicable task records.

## Reconciliation rule

At each material feature change, reconcile this roadmap against current repository implementation state, applicable platform requirements, acceptance evidence, and GoreeCloud Tasks Management. Missing obligations, stale status, duplicated work, roadmap drift, or undocumented disposition changes are defects to correct.
