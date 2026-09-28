# AIEngineeringStandard Jupyter Plugin

This package adds a Jupyter/IPython runtime adapter to AIEngineeringStandard 2.0 while keeping the portable Agent Plugin package separate from notebook execution.

The portable plugin uses the Agent Plugins 1.0.0 plugin.json contract. The runtime adapter follows the normal IPython extension mechanism: install the package, then load it with %load_ext.

## Install from the repository

From a notebook:

~~~python
%pip install "git+https://github.com/eaglesjo/codingStandard-dev.git#subdirectory=plugins/jupyter-notebook"
~~~

Then reload the kernel if the environment requires it and run:

~~~python
%load_ext aies_jupyter
%aies status
~~~

## Commands

| Command | Purpose |
|---|---|
| %aies status | Compact standard/runtime status |
| %aies profile | Full measured runtime profile |
| %aies validate | Run the repository validation entrypoint |
| %aies report | Persist a runtime report under .codingstandard/ |

The adapter is deliberately lightweight. It does not silently install packages, change the kernel, modify notebook cells, or access credentials.

## Relationship to Colab

Colab remains a specialized hosted-runtime policy under platform/colab. The Jupyter plugin is the notebook-facing adapter and can run in local Jupyter, VS Code notebooks, JupyterLab, and Colab. Colab-specific persistence and runtime guidance continues to come from the Colab platform layer.
