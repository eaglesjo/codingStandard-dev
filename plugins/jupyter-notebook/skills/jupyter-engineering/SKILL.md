---
name: jupyter-engineering
description: Apply AIEngineeringStandard 2.0 lifecycle, runtime, reproducibility, and validation rules inside Jupyter/IPython notebooks.
---

# Jupyter Engineering Skill

Use this Skill when an AI agent is working inside a Jupyter Notebook or IPython runtime.

## Runtime contract

1. Measure the active Python/kernel runtime; do not infer it from the user's desktop OS.
2. Resolve the AIEngineeringStandard root from the current project or AIENGINEERINGSTANDARD_ROOT.
3. Treat accelerators, RAM, disk, and hosted-runtime lifetime as measured capabilities.
4. Keep notebook cells runnable from a fresh kernel.
5. Avoid hidden state, duplicate dependency installation, and unbounded output growth.
6. Keep durable artifacts, checkpoints, metadata, and logs outside ephemeral runtime storage when the environment is ephemeral.
7. Run the standard validation entrypoint before claiming conformance.

## Jupyter adapter

After installing the Jupyter adapter:

~~~python
%load_ext aies_jupyter
%aies status
%aies profile
%aies validate
%aies report
~~~

%aies report writes .codingstandard/jupyter-runtime.json and records the measured runtime without storing secrets.

## Boundaries

The adapter does not grant filesystem, network, GitHub, cloud, or secret access. Those permissions remain controlled by the notebook runtime and the agent/client executing the notebook.
