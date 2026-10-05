# GoreeCloud for Zorin OS — Project Record

**Repository:** `GoreeCloud/zorin-os`  
**Lifecycle:** Development  
**Record purpose:** Significant project, desktop, Care, security, governance, migration, release, and acceptance history  
**Canonical authority after acceptance:** this file on the repository authoritative/default branch

## Project direction

GoreeCloud for Zorin OS developed as the first-party workstation experience for the verified Zorin OS environment. The repository owns the GoreeCloud desktop themes/assets, installation/recovery tooling, and workstation-specific application work that belongs with the desktop platform.

The desktop direction is light-first. Dark and Deep Dark variants remain compatibility surfaces rather than the primary visual identity.

GoreeCloud Care is maintained under `apps/goreecloud-care/` as a first-party local maintenance application within this repository.

## Historical Care Development path

Care evolved through a Development line that established preview-first cleanup, truthful Linux cache semantics, local reporting, Maintenance Insights, accessibility behavior, deterministic packaging, exact source provenance, isolated installed launchers, PolicyKit privilege separation, rollback, and platform-status boundaries.

Historical dev20/dev21/dev22 and earlier exact-candidate evidence remains useful regression evidence but does not transfer automatically to later source/package identities.

## September 7, 2026 — Stable Care 0.1.0

Care `0.1.0` was promoted as an exact immutable Stable release artifact rather than rebuilt during governance promotion.

Historical release evidence includes:

- exact source `bbc4779454c2887b810aa0ddc9e8a686a4c68ebd`;
- released package SHA-256 `819cff6e0132bf6b09df0986682995c25b14c39e74982f725efd0b5a21b71160`;
- Zorin OS 17.3 representative install/lifecycle acceptance;
- real-desktop PolicyKit cancellation and success coverage for APT cleanup and file-cache reclaim;
- Privacy Shield exact-build acceptance for the bounded Care privacy scope;
- Wardveil exact-build adoption with protection permission limited to the local-maintenance privilege boundary;
- Everkeep exact-build continuity governance; and
- Glaze UI V1.2 exact-source consumer acceptance.

Those approvals are historical exact-identity evidence. They do not authorize the current `0.2.0` Development line.

The release-scoped detail remains in `apps/goreecloud-care/SPECIFICATIONS.md`, `RELEASE-ACCEPTANCE.md`, `RECOVERY.md`, `SECURITY.md`, `PRIVACY.md`, and related Git history.

## September 13–16, 2026 — Care 0.2 Development line

Care began the `0.2.0` Development line so major presentation/platform changes would receive a new source/runtime/package identity rather than silently replacing Stable `0.1.0`.

The line progressed through dev1/dev2/dev3 work, including Glaze UI V1.4-era implementation, stronger optical/accessibility behavior, current package lifecycle and reproducibility controls, and continued fail-closed platform authority.

Historical dev2 evidence remains scoped to its exact source/package and is not current authority.

## September 27, 2026 — dev3 qualification reconciliation

Care PR #17 was reconciled after stale test and validation assertions still treated Glaze 1.4.1 as the required target.

The Development branch corrected those stale assertions while retaining V1.4.1 as the active implementation and treating newer shared Glaze versions as migration targets rather than inherited acceptance.

A fully qualified pre-project-governance checkpoint was established at:

- source `9e87abca338dfd40efaafd90de71811e88e97939`;
- runtime/package `0.2.0-dev3` / `0.2.0~dev3`;
- package SHA-256 `ab64ecce44d2cb8c3bca6a974743d07f36b6d47e7265598cf8725956fad0f352`;
- Care qualification run `36356767130`;
- theme-source run `36356767132`;
- legacy Platform Contract run `36356767472`; and
- primary qualification artifact `10944506742`.

All three workflows succeeded for that exact checkpoint. Because source identity is exact, later changes—including this project-governance migration—must receive fresh qualification and package provenance.

## September 27, 2026 — current platform authority reconciliation

Live shared Glaze authority was reverified as GLAZE UI V1.6 / `1.6.0` Official Anchor.

Care still implements V1.4.1 and its legacy manifest names 1.5.0 as a required target. The project therefore records Care as migration-required rather than current Glaze-conformant.

Current central Platform Contract authority is `2.0` with the current nine-system model and Seed/Lab/Forge/Weave/Seal/Anchor/Sunset/Archive lifecycle vocabulary.

Care's checked-in Contract 0.2 manifest remains versioned legacy evidence until an explicit migration. Historical lifecycle and seven-system semantics are not mechanically reinterpreted as Contract 2.0 truth.

## September 27, 2026 — Wardveil dev3 review

Wardveil issue #177 reviewed the Care dev3 local-maintenance privilege boundary.

Source/install/lifecycle evidence confirmed the fixed helper path, fixed allow-listed actions, PolicyKit fail-closed behavior, isolated launchers, root-owned package/policy/provenance boundaries, and `protected_by_wardveil=false`.

The authority decision remains **CHANGES REQUIRED** because exact-candidate representative Zorin OS 17.3 native/PolicyKit acceptance has not yet been supplied for the current Development source/package.

No production protection, cross-service execution authority, release, or lifecycle promotion was granted.

## September 27, 2026 — Drive source reconciliation

The portable `Project Specification — Care.docx` migration source was reconciled to current verified state as v0.16.

The retained native Google Docs predecessor was audited against the portable source. The documents contain the same normalized paragraph count; differences are current-state replacements rather than evidence of missing unique substantive Care requirements. No comments or exact-ID references were found in the native document during the audit.

Both Drive sources remain retained because the mandatory repository-local `PROJECT-SPECIFICATIONS.md` / `PROJECT-RECORD.md` migration and default-branch readback had not yet completed. Migration first, verification second, Drive removal last.

## September 27, 2026 — repository-local project governance migration

This candidate adds the mandatory root `PROJECT-SPECIFICATIONS.md` and `PROJECT-RECORD.md` required by the GoreeCloud Project Specifications and Project Records Repository standard.

The migration treats the repository—not Care alone—as the project boundary. It therefore records both the Zorin desktop experience and Care component while preserving the detailed historical Stable Care specification as release-scoped supplementary evidence.

The root README is cross-referenced to these files and the Care release specification is explicitly marked historical so it cannot compete with current repository authority.

This migration is not complete until accepted on the authoritative/default branch and read back. The Drive sources must remain until that verification succeeds.

## Repository governance boundary

As of the September 27 migration review, the repository default `main` branch is not protected. No repository-specific protection issue was found during the current lookup.

The centralized GoreeCloud GitHub protection task therefore remains applicable. Until live protection is verified, source integration must continue through bounded branches, exact-head CI, appropriate review, guarded merge behavior, and post-merge readback rather than treating successful workflows as equivalent to repository enforcement.

## Ongoing record maintenance

Update this record for significant:

- repository or component scope changes;
- Zorin target changes;
- desktop architecture or installer/recovery transitions;
- Care architecture or privilege-boundary changes;
- major privacy/security/recovery decisions;
- Glaze UI or Platform Contract migrations;
- representative-target acceptance;
- production/release/lifecycle transitions;
- repository governance changes;
- significant incidents or rollbacks; and
- eventual deprecation or retirement.

Routine implementation detail belongs in the applicable changelog, Git history, issues, and pull requests.
