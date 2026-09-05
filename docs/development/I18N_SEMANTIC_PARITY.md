# i18n Semantic Parity

v1.16 defines semantic parity as equality of engineering intent, not equality of translated sentences.

## Canonical policy intents

| Intent | Meaning |
|---|---|
| `environment.validate` | Validate the real execution environment and runtime conditions before resource-sensitive decisions. |
| `resources.memory.measure` | Measure memory and resource availability instead of relying on named hardware assumptions. |
| `tasks.early_stopping` | Use Early Stopping where meaningful for long-running workloads. |
| `recovery.checkpoint` | Persist the best or recoverable Checkpoint so long-running work can resume. |
| `behavior_change.tests` | Validate behavior changes with meaningful tests, beginning with the smallest meaningful test. |

## Validation model

The English repository is the canonical policy source. Each policy intent maps to one or more stable semantic concepts. The existing locale concept catalog supplies language-specific expressions for those concepts.

```text
English canonical policy
        ↓
Policy intent ID
        ↓
Canonical semantic concept
        ↓
Locale vocabulary
        ↓
Localized policy resource
```

A translation can use different sentence structure, terminology, or word order. It must still express the required engineering concept.

## Why this is stronger than string comparison

Sentence-level comparison produces false failures because natural languages differ in grammar and structure. It can also produce false confidence when a translated sentence contains familiar words but changes the policy meaning.

Semantic parity therefore checks whether the canonical document expresses a required concept and whether the localized document expresses the corresponding locale concept.

## Runtime requirement

All runtime locales in `i18n/quality.json` must satisfy semantic parity. A missing required concept is a release-gate failure and cannot be hidden by the English fallback.
