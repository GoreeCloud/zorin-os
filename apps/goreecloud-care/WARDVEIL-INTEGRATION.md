# GoreeCloud Care — Wardveil Security Integration

## Scope

GoreeCloud Care uses the current Wardveil Security status semantics for a narrowly scoped security-evidence producer covering the installed Care privileged-maintenance boundary. This integration does not make Wardveil the executor of Care maintenance, does not grant Wardveil arbitrary command authority, and does not authorize a broad `Protected by Wardveil` product claim.

## Authoritative producer

GoreeCloud Care is authoritative only for these Care-owned facts:

- the installed fixed helper location;
- the installed Care PolicyKit policy location;
- whether those fixed files satisfy the expected root-ownership and write-permission constraints;
- whether `/usr/bin/pkexec` is available for the existing PolicyKit flow;
- the source-enforced helper action allowlist and no-arbitrary-shell/path boundary;
- whether the installed application/helper launchers use isolated Python path semantics so a user-controlled working directory, `PYTHONPATH`, or user site cannot shadow the installed Care package;
- whether the fixed private Care Python package directory is free of stale runtime bytecode that could affect cross-version execution.

PolicyKit, the operating system, and APT remain authoritative for their own behavior. Wardveil Security remains authoritative for Wardveil security semantics and any future Wardveil-native policy, scanning, quarantine, incident, or audit service.

## Installed launcher isolation

Representative dev18 package-lifecycle testing found that the pre-dev19 launchers used plain `python3 -m goreecloud_care...`. When the installed package had been downgraded to dev17 but the command was launched from a newer source directory, Python could resolve the working-tree package instead of the installed package. The privileged helper used the same ambient import pattern, so this was treated as a security-boundary defect rather than merely a test-harness issue.

Dev19 changed both installed entrypoints to `/usr/bin/python3 -I -B -m ...`. `-I` excludes the current working directory, `PYTHONPATH`, and user site from import resolution; `-B` prevents new runtime bytecode writes. Debian `postinst`/`postrm` scripts remove only the fixed private Care `__pycache__` path so bytecode created by earlier Development versions cannot survive an install/remove transition. Installed acceptance deliberately attempts same-named working-directory shadowing against both entrypoints.

Representative dev20 package-lifecycle evidence accepted that remediation on the Zorin OS target through install, remove, fresh reinstall, downgrade to accepted dev17, restore, and final-state validation. Dev22 retains the same boundary.

## Local status API

`goreecloud-care --security-status-json` returns a Wardveil-compatible `0.1.0` status record for the local Care privilege boundary.

A passing result requires the fixed helper and policy files to be regular files owned by the expected root UID, neither file to be group/world writable, the helper to be owner-executable, and `/usr/bin/pkexec` to be executable. Missing or non-passing evidence produces `attention` rather than a passing state.

The record is explicitly scoped to application `goreecloud-care`, identifies `GoreeCloud Care` / `local-maintenance-privilege-boundary` as the Care-owned authority, carries an observation timestamp and a short passing validity window, and fails closed when current evidence is unavailable.

The record deliberately sets `claim.protected_by_wardveil` to `false`. Care must not display or advertise `Protected by Wardveil` merely because it emits a Wardveil-compatible status record.

## Privacy boundary

The shared record omits user identity, arbitrary local file paths, raw privileged command output, credentials, secrets, private keys, recovery material, and unrestricted diagnostics. It reports only the scoped normalized state, observation/freshness data, a short summary, and explicit redaction metadata.

## Failure and freshness behavior

Missing helper/policy/pkexec evidence fails closed to a non-passing state. Writable privileged-boundary files also fail closed. A passing record receives a 15-minute validity interval so stale evidence cannot remain indefinitely reassuring. Consumers must re-evaluate after expiry.

State is communicated through explicit text fields (`state`, `source_state`, summary, authority and scope), so the evidence does not depend on color or iconography alone.

## High-impact actions

Care does not currently accept Wardveil runtime-authorization envelopes for `apt-clean`, file-cache reclaim, user-file cleanup, or Trash deletion. Existing Care actions retain their explicit local user confirmation, PolicyKit, ownership, fixed-allowlist, and application-specific authorization boundaries. Therefore Wardveil's high-impact cross-service executor requirements are not claimed as implemented by this integration.

## Exact-source automated prequalification

Latest completed exact-candidate prequalification checkpoint before this documentation reconciliation:

- source revision: `188a60c5277f5b2d9a9b6499ba500b5340dd8eb6`;
- runtime: `0.2.0-dev3`;
- Debian package: `0.2.0~dev3`;
- package SHA-256: `5a4aab81c4869a068f075371d1e6e94bcef25fcdca217ac3fdd429860f81451a`;
- Care qualification: run `36356321253` — success;
- theme-source validation: run `36356321241` — success;
- Platform Contract validation: run `36356321526` — success;
- primary qualification artifact: `10944555293`.

This file is itself part of the packaged source. Any edit to it creates a new source/package identity, so the checkpoint above must not be relabeled as evidence for a later PR head. Live GitHub PR #17 and its exact-head workflows are authoritative for the current candidate identity and qualification state.

The exact-head qualification passed source/unit/contract validation, headless GTK task-flow and accessibility checks, package construction and inspection, same-source and Ubuntu 22.04/24.04 cross-environment reproducibility, immutable Stable `0.1.0` rollback reconstruction, installed package lifecycle, launcher-isolation checks, PolicyKit success/cancellation/failure outcome mapping, and installed Wardveil-compatible privilege-boundary prequalification.

The installed package keeps the privileged boundary narrow:

- `/usr/lib/goreecloud-care/goreecloud-care-helper` and the PolicyKit policy are fixed package-owned paths;
- the PolicyKit rule denies inactive/any-user authorization and requires administrator authentication for active use;
- the helper accepts only `apt-clean` and `reclaim-memory`;
- `apt-clean` invokes fixed argv `/usr/bin/apt-get clean`;
- file-cache reclaim writes only the fixed value `3` to `/proc/sys/vm/drop_caches`;
- installed application/helper launchers use `/usr/bin/python3 -I -B -m ...`;
- package lifecycle validation repeats isolated-launcher and bounded security-status checks across install, remove, reinstall, Stable downgrade, and restore; and
- Care continues to emit `claim.protected_by_wardveil=false`.

This evidence is source/install/lifecycle prequalification, not representative-target Wardveil acceptance. It does not grant production protection, cross-service execution authority, release status, or lifecycle promotion.

Wardveil review issue `GoreeCloud/wardveil#177` records the latest authority decision. The remaining Wardveil-specific evidence gap is exact-candidate representative Zorin OS 17.3 native/PolicyKit acceptance for the then-current PR #17 source/package identity. Historical Stable/dev1/dev2 target evidence does not transfer, and any later source/package identity requires fresh exact-head validation and review binding.

## Acceptance boundary

Care-side source evidence now covers the Wardveil adoption requirements that can be automated locally: integration documentation, protected/non-passing status behavior, missing/writable fail-closed behavior, freshness, explicit text semantics, sensitive-field minimization, launcher isolation, private-bytecode cleanup, and exact-source CI evidence.

Still required before any Wardveil protection claim or production-conformant Wardveil status:

- exact-candidate representative Zorin OS 17.3 installed-boundary and native PolicyKit acceptance for the current PR #17 source revision and its exact qualified package SHA-256;
- any remaining security-relevant desktop PolicyKit-agent acceptance required by release policy;
- exact-candidate Privacy Shield acceptance where it affects the shared security-evidence boundary;
- governed Wardveil adoption/promotion explicitly permitting the narrowly scoped claim; and
- fresh review if the source, package bytes, helper/policy behavior, or relevant evidence changes.

Until those steps complete, `goreecloud.platform.yaml` must remain fail-closed and `claim.protected_by_wardveil` must remain `false`.
