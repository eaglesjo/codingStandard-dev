# AI Engineering Standard

<p align="center">
  <strong>AI Development, Training & Agent Engineering Standards</strong>
</p>

<p align="center">
  <strong>v1.17.2</strong>
</p>

<p align="center">
  <a href="https://github.com/eaglesjo/AIEngineeringStandard/releases"><img src="https://img.shields.io/github/v/release/eaglesjo/AIEngineeringStandard?label=public%20release" alt="Public release"></a>
  <a href="https://github.com/eaglesjo/codingStandard-dev/actions/workflows/validate-coding-standard.yml"><img src="https://github.com/eaglesjo/codingStandard-dev/actions/workflows/validate-coding-standard.yml/badge.svg?branch=main" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT License"></a>
</p>

**Language:** English · [한국어](i18n/ko/README.md) · [Français](i18n/fr/README.md) · [Español](i18n/es/README.md) · [简体中文](i18n/zh-CN/README.md) · [日本語](i18n/ja/README.md) · [Русский](i18n/ru/README.md) · [Türkçe](i18n/tr/README.md) · [Deutsch](i18n/de/README.md) · [Italiano](i18n/it/README.md) · [Português](i18n/pt/README.md) · [العربية](i18n/ar/README.md) · [हिन्दी](i18n/hi/README.md) · [Bahasa Indonesia](i18n/id/README.md) · [Tiếng Việt](i18n/vi/README.md) · [ไทย](i18n/th/README.md) · [Nederlands](i18n/nl/README.md) · [Polski](i18n/pl/README.md) · [Svenska](i18n/sv/README.md) · [Українська](i18n/uk/README.md)

> **Repository model:** `codingStandard-dev` is the public development, validation, and release source of truth. Validated releases are promoted to `eaglesjo/AIEngineeringStandard`. `codingStandard-private` is reserved for Luna-only resources and is not a release source.

> **Runtime resource languages:** 20 locales are validated for runtime resources: English, Korean, French, Spanish, Simplified Chinese, Japanese, Russian, Turkish, German, Italian, Portuguese, Arabic, Hindi, Indonesian, Vietnamese, Thai, Dutch, Polish, Swedish, and Ukrainian.

> **v1.16 quality contract:** runtime locales must satisfy resource completeness, semantic policy parity, and runtime/documentation consistency before release promotion.

## Release model

Development, validation, and release preparation happen in `codingStandard-dev`. Validated public releases are promoted to `AIEngineeringStandard`. The private `codingStandard-private` repository is reserved for Luna-only continuity, recovery, and fallback resources.

## What is AI Engineering Standard?

`AI Engineering Standard` is a reusable engineering standard for AI-assisted development, model training, experimentation, LLM/Vision workflows, general ML/DL workflows, and AI coding agents.

It provides:

- canonical project instructions with thin per-tool adapters;
- common ML/DL lifecycle guidance;
- LLM and Vision domain guidance;
- task-specific Skills;
- environment and resource detection;
- Google Colab execution/recovery policy;
- cross-platform installers;
- multilingual runtime resources and documentation;
- validation and installer test suites;
- architecture and policy profiles;
- semantic policy intent validation;
- runtime/documentation consistency validation;
- reproducible training and experiment guidance.

## Supported AI Development Tools

The repository provides project-level adapters, instruction files, Skills, or documented integration paths for a broad set of AI development tools.

## Supported Development Environments

AI Engineering Standard is designed to work across local Python development, interactive notebook workflows, cloud notebooks, and AI-assisted IDE workflows.

| Environment / Tool | Support |
|---|---|
| Python | Core |
| Jupyter Notebook | Supported |
| Google Colab | Supported |
| Visual Studio Code | Supported |

### Platform support

| Platform | Role |
|---|---|
| Linux | Supported platform |
| Ubuntu 24.04 LTS | Linux CI reference environment |
| macOS | Supported and validated by CI |
| Windows | Supported and validated with Windows PowerShell and PowerShell 7 |
| Google Colab | Supported ephemeral cloud execution target |

## Quick Start

Clone the public distribution repository in the project you want to configure:

### Windows / PowerShell

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

### Linux / macOS

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Available domains:

```text
common | ml | llm | vision | colab | all
```

## Repository Structure

The repository uses a canonical layered structure with shared policy, domain resources, platform policy, installers, validation, tests, profiles, and multilingual runtime resources.

```text
.
├── core/
├── domains/
│   ├── ml/
│   ├── llm/
│   └── vision/
├── platform/
│   └── colab/
├── examples/
│   └── colab/
├── docs/
│   ├── development/
│   └── releases/
├── i18n/
├── profiles/
├── scripts/
│   ├── development/
│   ├── installers/
│   └── validation/
├── tests/
│   └── validation/
├── .github/
└── VERSION
```

## Environment, ML, and Colab Policy

Runtime decisions are based on measured capabilities rather than a named machine profile. The shared profiler considers OS, Python/runtime, CPU, RAM, disk, accelerators, VRAM, CUDA/ROCm/MPS/DirectML, precision capability, and Jupyter/Colab state.

For Google Colab, `platform/colab/` treats the notebook VM as ephemeral: dependency bootstrap, measured resource resolution, smoke testing, durable checkpointing, artifact persistence, and resume validation are first-class controls.

## Architecture and Policy Profiles

Architecture and policy profiles make layer boundaries, dependency direction, repository-wide rules, runtime assumptions, and scalability characteristics explicit and machine-readable.

- `profiles/project.json` — project-level runtime, delivery, and scalability profile.
- `profiles/architecture/repository-standard.json` — canonical layers and dependency directions.
- `profiles/policies/repository-default.json` — repository-wide validation, testing, reproducibility, platform, secrets, and network rules.

## i18n Quality and Semantic Policy

The multilingual contract covers 20 runtime locales and validates resource completeness, semantic policy parity, and runtime/documentation consistency.

Runtime locales must achieve quality grade **A** before release promotion.

The canonical policy intent vocabulary currently covers:

- `environment.validate`
- `resources.memory.measure`
- `tasks.early_stopping`
- `recovery.checkpoint`
- `behavior_change.tests`

## Validation

Run the relevant checks before publishing a release:

```bash
python scripts/validation/validate_profiles.py
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

GitHub Actions validates the release gate on Ubuntu 24.04 LTS. The gate covers architecture, repository structure, environment contracts, installers, multilingual resource quality, runtime/documentation consistency, and CPU smoke tests.

## Documentation

- [Installation Guide](INSTALL.md)
- [Korean README](i18n/ko/README.md)
- [Language Resources](i18n/README.md)
- [Architecture Profiles](docs/development/ARCHITECTURE_PROFILES.md)
- [Policy Inheritance](docs/development/POLICY_INHERITANCE.md)
- [Project Profiles](docs/development/PROJECT_PROFILES.md)
- [Release Notes](docs/releases/RELEASE_NOTES.md)
