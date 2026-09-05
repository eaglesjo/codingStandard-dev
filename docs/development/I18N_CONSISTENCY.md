# i18n Runtime / Documentation Consistency

v1.16 treats the runtime locale catalog and locale documentation as one release contract.

## Consistency requirements

For every required runtime locale:

1. The locale must exist in `i18n/languages.json` under `runtime_resources`.
2. The locale must exist in `i18n/quality.json` under `required_runtime_locales`.
3. The locale runtime resource directory must exist.
4. The required common policy resources must exist:
   - `core/common/AGENT.md`
   - `core/common/SKILL.md`
   - `core/common/ENVIRONMENT.md`
5. The locale must have a documentation catalog entry.
6. The documented locale display name must appear in the corresponding README.
7. The README must explicitly describe runtime support and state the current runtime locale count.

## Why this is a release gate

A locale can be technically complete while its documentation still describes an older support model. That creates a contract mismatch for users and maintainers.

The consistency validator prevents stale claims such as "docs-only", "runtime support pending", or an outdated locale count from surviving a release.

## Validation

```bash
python scripts/validation/check_i18n_consistency.py
```

The release validator runs this check together with resource completeness and semantic parity validation.
