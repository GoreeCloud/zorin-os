# GoreeCloud for Zorin OS — Project Specifications

**Repository:** `GoreeCloud/zorin-os`  
**Project type:** First-party Zorin OS desktop experience plus workstation-specific applications  
**Lifecycle:** Development  
**Verified representative platform:** Zorin OS 17.3  
**Primary application component:** `apps/goreecloud-care/`  
**Current shared Glaze authority:** GLAZE UI V1.6 / `1.6.0` Official Anchor; project-local consumer acceptance remains separate  
**Current Platform Contract authority:** `2.0`; legacy component manifests retain their own historical/versioned semantics until explicitly migrated  
**Canonical project authority after acceptance:** this file together with `PROJECT-RECORD.md`

## 1. Governance and precedence

This repository must be sufficient to understand the GoreeCloud Zorin OS project, its Care application, current requirements, material history, and acceptance boundaries.

Current verified source and runtime evidence controls implementation claims. Historical Drive documents, historical Care release records, older Glaze targets, and predecessor repository names are evidence only and must not override live accepted repository state.

This repository-local migration is not complete merely because these files exist on a branch. The files become authoritative only after the migration is accepted on the repository's authoritative/default branch and read back successfully. Until that gate is met, the retained migration sources remain protected from deletion.

## 2. Project purpose

GoreeCloud for Zorin OS provides a first-party, light-first GoreeCloud desktop experience for the verified Zorin OS environment and hosts workstation-specific applications that belong with that platform experience.

The project currently includes two major responsibility areas:

1. the GoreeCloud desktop/theme/icon/cursor/wallpaper experience and its safe installer/recovery tooling; and
2. GoreeCloud Care, a local-first maintenance application under `apps/goreecloud-care/`.

The project must preserve Zorin OS as the underlying operating-system authority. It must not redistribute or silently replace unsupported Zorin base-theme/system bytes, invent target compatibility, or claim acceptance from source presence alone.

## 3. Desktop experience scope

The desktop project must maintain:

- `GoreeCloud-Zorin-Light` as the primary application/shell experience;
- Dark and Deep Dark compatibility variants where supported;
- the GoreeCloud icon theme and cursor theme;
- GoreeCloud wallpaper source derivatives and the governed visible wallpaper catalog;
- exact target-package and base-file validation before composition or replacement;
- package-safe stock-wallpaper replacement through controlled diversion rather than destructive removal of required Zorin desktop packages;
- recoverable install, replacement, restoration, and uninstall behavior; and
- explicit failure when the local platform is outside the verified target boundary.

The current desktop asset implementation retains repository-local legacy Glaze palette work. Current shared Glaze authority is V1.6 / 1.6.0, so repository-local desktop presentation must not be represented as current Glaze-conformant without an explicit current-target reconciliation and acceptance record.

## 4. GoreeCloud Care role and scope

GoreeCloud Care is GoreeCloud's first-party, local-first desktop maintenance application for Zorin OS and compatible GTK 3 environments.

Care is designed around:

- preview-first maintenance;
- explicit user confirmation;
- least privilege;
- truthful Linux system-state language;
- local-first operation;
- privacy-minimized reports and status;
- accessible native interaction;
- deterministic packaging and exact provenance;
- fail-closed security/privacy/recovery evidence; and
- exact-candidate acceptance rather than inherited historical approval.

Care must not represent ordinary Linux page/file cache as inherently harmful or promise a permanent performance boost from cache reclaim.

### 4.1 Maintenance capabilities

Care may provide, within the accepted implementation scope:

- read-only scanning of stale application cache;
- thumbnail-cache preview and cleanup;
- bounded scanning/cleanup of eligible user-owned stale temporary files;
- Trash preview and separately confirmed permanent emptying;
- APT package-cache preview and PolicyKit-authorized cleanup;
- disk, available-memory, and Linux file-cache status;
- separately warned and PolicyKit-authorized Linux file-cache reclaim;
- explicit cancellation, denial, failure, partial-success, and completion states;
- post-action refresh that preserves final operation outcome;
- privacy-safe human-readable and machine-readable reports;
- bounded read-only Maintenance Insights; and
- local health, Privacy Shield-shaped, Wardveil-compatible, and continuity status interfaces.

Scanning must not delete by itself.

## 5. Security and privilege requirements

The ordinary Care GTK process must not run as root.

Routine user-cache and temporary-file cleanup remains unprivileged. Privilege is restricted to the fixed package-owned helper and approved PolicyKit action.

The privileged helper must:

- accept only the explicitly allow-listed `apt-clean` and `reclaim-memory` operations;
- accept no arbitrary filesystem path, shell command, shell fragment, or user-supplied executable;
- invoke APT cleanup with fixed argv;
- write only the approved fixed reclaim value to the fixed Linux cache-control path;
- fail closed for unsupported actions;
- preserve explicit authorization cancellation/denial/failure outcomes; and
- remain isolated from invoking-directory, `PYTHONPATH`, user-site, and same-named-package shadowing.

Package-owned helper, policy, provenance, launcher, and maintainer-script paths must retain appropriate root ownership, non-writable boundaries, and fixed locations.

Trash deletion remains an irreversible Care-owned action and requires separate explicit confirmation.

## 6. Privacy requirements

Care core maintenance functionality must remain usable without telemetry, analytics, cloud tracking, remote context, or network access.

Default report/status output must minimize local information and omit raw private content, candidate paths, filenames, raw scan-error strings, reusable secrets, and unnecessary identifiers.

Maintenance Insights may expose home-relative paths only inside the deliberately opened local review surface. Discovery must remain bounded and must not follow symlinks.

Privacy Shield remains the separate privacy authority. Care source, tests, or local status cannot self-grant Privacy Shield acceptance.

## 7. Accessibility and interface requirements

Care and desktop surfaces must preserve:

- keyboard reachability and visible focus;
- assistive-technology names/roles/status semantics;
- enlarged-text and effective-width behavior;
- High Contrast/system authority;
- Reduced Motion and Reduced Transparency behavior;
- non-color-only status meaning;
- safe error/cancellation states;
- compact and wider desktop compositions where applicable; and
- honest lifecycle/authority language.

Care currently retains a qualified V1.4.1 Optical Intelligence implementation. Its legacy manifest names 1.5.0 as a required target, while current shared Glaze authority is V1.6 / 1.6.0 Official Anchor. Care therefore remains current-target migration-required and requires fresh application-specific rendered/native/accessibility/performance acceptance after migration.

## 8. Data, storage, and recovery

Care must not create a substantial durable application-owned user dataset merely to perform maintenance.

Authoritative Care continuity centers on:

- exact source/package provenance;
- install/remove/reinstall behavior;
- controlled downgrade and restore;
- protected representative-target evidence where required;
- truthful irreversible-maintenance boundaries; and
- separate Everkeep authority for continuity promotion.

Missing, malformed, writable, symlinked, source-mismatched, package-mismatched, stale, or unpromoted recovery evidence must fail closed.

The desktop installer must preserve recoverable copies or controlled diversions before replacing governed desktop assets.

## 9. Platform integrations

Care's platform integrations must remain authority-separated.

- **Glaze UI:** presentation authority only; Care requires current-target migration and application-specific acceptance.
- **Privacy Shield:** privacy/data-use authority; exact-candidate decision required before production privacy claims.
- **Wardveil Security:** security/protection governance; Care remains the technical authority for its own local maintenance actions. Wardveil may permit only explicitly accepted protection claims and must not receive cross-service execution authority by implication.
- **Everkeep:** recovery/continuity authority; Care cannot self-promote continuity readiness.
- **Manager, Mesh, Identity, Policy, Observability, and other current Platform Contract systems:** applicability must be evaluated under the current Contract version rather than copied from legacy seven-system semantics.
- **GoreeCloud Sync:** separately governed; it must not be manufactured as an Integral Platform System solely to satisfy a version migration.

The checked-in Care manifest still uses legacy Platform Contract 0.2 semantics. Migration to current Platform Contract 2.0 and the current nine-system model must be explicit, evidence-backed, and fail closed for producer-domain acceptance that Care cannot prove.

## 10. Packaging and provenance

Care Development and release packages must preserve deterministic and inspectable provenance.

Applicable requirements include:

- authoritative Git source identity;
- rejection of untracked package inputs;
- package-owned exact-source provenance;
- deterministic timestamps and normalized staged modes;
- same-source reproducibility;
- cross-environment reproducibility where governed;
- caller-umask independence;
- fixed package-owned launcher/helper/policy locations;
- exact package SHA-256 recorded outside the package where circular self-hashing would otherwise result; and
- exact-candidate evidence renewal after any source change.

The immutable historical Stable `0.1.0` package remains exact-release evidence. Later Development source does not inherit its acceptance automatically.

## 11. Deployment and operations

Desktop installation must fail closed outside the verified Zorin target boundary and must preserve a recovery path.

Care installation/upgrade must validate package identity, provenance, launcher isolation, fixed privilege paths, and removal/reinstall/rollback behavior as applicable.

Production or Anchor status requires exact deployment identity, rollback/recovery evidence, appropriate monitoring/diagnostics, representative target validation, current platform-system decisions, and explicit lifecycle authority.

## 12. Testing and acceptance

Source/CI success is not production acceptance.

Material Care candidates must receive applicable evidence across:

- unit and contract tests;
- source/schema validation;
- GTK runtime behavior;
- safe maintenance task flow;
- AT-SPI/accessibility behavior;
- appearance/accessibility fallbacks;
- package build and inspection;
- deterministic/reproducible package verification;
- installed lifecycle;
- privilege-boundary prequalification;
- representative Zorin OS 17.3 native/PolicyKit behavior where required;
- exact package provenance;
- platform-system authority decisions;
- rollback/recovery; and
- post-integration authoritative readback.

Human/manual/physical-device evidence must not be fabricated from automation.

## 13. Current Development boundary

The active Care `0.2.0-dev3` line is Development and nonconformant. Live PR #17 and its exact-head workflows control the current candidate identity.

The last fully qualified pre-migration checkpoint before these repository-governance files was source `9e87abca338dfd40efaafd90de71811e88e97939`, package `0.2.0~dev3`, SHA-256 `ab64ecce44d2cb8c3bca6a974743d07f36b6d47e7265598cf8725956fad0f352`. Any source change, including this governance migration, creates a new exact candidate and requires fresh qualification/provenance.

Current known gates include:

- current Glaze V1.6 migration and Care-specific consumer acceptance;
- explicit Platform Contract 2.0 migration/reclassification;
- exact-candidate representative Zorin OS 17.3 native/PolicyKit evidence;
- fresh Privacy Shield decision;
- fresh Wardveil decision after representative evidence;
- fresh Everkeep decision;
- appropriate independent review and repository protection/integration controls;
- authoritative post-merge readback; and
- explicit later release/production/Anchor qualification.

## 14. Historical Stable Care release

Care Stable `0.1.0` remains immutable historical release evidence for its exact source/package and accepted Zorin OS 17.3 target.

The detailed release-scoped specification remains in `apps/goreecloud-care/SPECIFICATIONS.md`. It is supplementary historical release evidence and does not replace this current repository-level specification.

## 15. Maintenance and retirement

Update this specification whenever material repository scope, desktop target behavior, Care requirements, platform integrations, security/privacy boundaries, packaging, supported targets, or acceptance rules change.

Significant historical decisions belong in `PROJECT-RECORD.md`; routine release/change chronology belongs in component changelogs.

Drive project-specification sources must not be removed until this migration is accepted on the authoritative/default branch, read back, verified complete, and free of unresolved migration discrepancies.
