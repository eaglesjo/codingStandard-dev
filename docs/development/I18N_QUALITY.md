# i18n Quality

v1.16 treats multilingual support as a quality contract, not only a resource-counting feature.

## Quality gates

Every runtime locale is evaluated against three gates:

1. **Resource completeness** — required runtime resources exist.
2. **Semantic parity** — required engineering-policy concepts are expressed in the locale using the locale vocabulary catalog.
3. **Runtime/documentation consistency** — the runtime locale and its documentation entry are both present and connected.

Runtime locales require quality grade **A**.

## Quality grades

| Grade | Meaning |
|---|---|
| A | Resource complete + semantic parity + runtime/documentation consistency |
| B | Resource complete + semantic parity; documentation gap remains |
| C | Resource complete; semantic parity gap remains |
| D | Resource or consistency gaps prevent a stronger grade |
| F | Contract or validation failure |

## Validation

```bash
python scripts/validation/check_i18n.py
python scripts/validation/check_i18n_quality.py
```

The release validator runs both checks automatically.

## Semantic policy model

Translations are not compared sentence-by-sentence. Instead, the canonical English policy declares a stable policy intent such as `environment.validate`, `resources.memory.measure`, `tasks.early_stopping`, `recovery.checkpoint`, or `behavior_change.tests`. Each locale provides vocabulary that can express that intent.

This keeps validation focused on engineering meaning rather than translation wording.
