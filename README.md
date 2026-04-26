<div align="center">

# 🌍 Global Job Market Intelligence Platform

### Real-Time Analytics · NLP Skill Extraction · ML Salary Prediction

[![CI](https://github.com/ArinPattnaik/global-job-market-intelligence-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/ArinPattnaik/global-job-market-intelligence-platform/actions)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**[🚀 Live Demo](https://global-job-market-intelligence-platform-arin.streamlit.app/)**

</div>

---

## Overview

An industrial-grade analytics platform that processes 5,000+ job postings across 8 countries, extracts skills using NLP, and predicts salaries with machine learning. Built with a modular architecture, comprehensive test suite, CI/CD pipeline, and production-ready Docker deployment.

## Features

| Module | Description |
|--------|-------------|
| **📊 Market Overview** | KPI dashboard with hiring trends, company breakdowns, and seniority distributions |
| **🧠 Skill Analytics** | NLP extraction of 80+ skills with category heatmaps and co-occurrence analysis |
| **💰 Salary Intelligence** | Box plots, percentile analysis, skill premiums, and top-paying company rankings |
| **🌍 Geographic Insights** | Choropleth maps, city-level analytics, and cross-country comparisons |
| **🔎 Job Explorer** | Multi-filter search with styled job cards, skill badges, and CSV export |
| **🤖 Salary Predictor** | GradientBoosting model with data-driven 95% confidence intervals |
| **📤 Universal Analyzer** | Upload any CSV/Excel for auto-analysis with smart visualizations |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│  │Market│ │Skill │ │Salary│ │ Geo  │ │ Job  │ │Salary│   │
│  │  Ovw │ │Analyt│ │Intel │ │Insght│ │Explor│ │Predct│   │
│  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘   │
│     └────────┴────────┴────────┴────────┴────────┘         │
│                         │                                   │
│              ┌──────────┴──────────┐                        │
│              │   Shared Utilities  │                        │
│              │ data_loader │ chart │                        │
│              │ ui_components       │                        │
│              └──────────┬──────────┘                        │
└─────────────────────────┼───────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────┐
│                    Backend Layer                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │   ETL    │  │   NLP    │  │ ML Model │  │  Config   │  │
│  │ Adzuna   │  │ 80+ Skill│  │ Gradient │  │ Settings  │  │
│  │ API +    │  │ Taxonomy │  │ Boosting │  │ Logging   │  │
│  │ Retry    │  │ + Regex  │  │ R²=0.93  │  │ Env-aware │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
# Clone
git clone https://github.com/ArinPattnaik/global-job-market-intelligence-platform.git
cd global-job-market-intelligence-platform

# Setup
python -m venv venv && source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Generate data (sample data included)
python data/generate_synthetic_data.py

# Run
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## Project Structure

```
├── app.py                          # Main landing page
├── pages/                          # Streamlit dashboard pages
│   ├── 1_Market_Overview.py
│   ├── 2_Skill_Analytics.py
│   ├── 3_Salary_Intelligence.py
│   ├── 4_Geographic_Insights.py
│   ├── 5_Job_Explorer.py
│   ├── 6_Salary_Predictor.py
│   └── 7_Data_Upload_Analyzer.py
├── config/                         # Configuration layer
│   ├── settings.py                 # Centralized settings & constants
│   └── logging_config.py           # Structured logging with rotation
├── utils/                          # Shared utilities (DRY)
│   ├── data_loader.py              # Validated data loading
│   ├── chart_helpers.py            # Plotly layout defaults
│   └── ui_components.py            # Reusable Streamlit components
├── nlp/
│   └── skill_extraction.py         # 80+ skill taxonomy with compiled regex
├── models/
│   └── train_model.py              # ML pipeline with cross-validation
├── etl/
│   └── fetch_jobs.py               # Adzuna API with retry logic
├── data/
│   ├── generate_synthetic_data.py  # Synthetic data generator
│   ├── raw/                        # Raw job postings
│   └── processed/                  # Processed with extracted skills
├── scripts/
│   └── update_pipeline.py          # End-to-end pipeline orchestrator
├── tests/                          # Comprehensive test suite (50 tests)
│   ├── conftest.py                 # Shared fixtures
│   ├── test_skill_extraction.py    # NLP tests
│   ├── test_data_generation.py     # Data quality tests
│   ├── test_model.py               # ML pipeline tests
│   └── test_chart_helpers.py       # Utility tests
├── assets/
│   └── style.css                   # Shared CSS theme
├── db/
│   └── schema.sql                  # PostgreSQL schema with indexes
├── .github/workflows/
│   ├── ci.yml                      # Lint + Test + Docker CI
│   └── release.yml                 # Auto-release on tags
├── Dockerfile                      # Multi-stage, non-root production image
├── pyproject.toml                  # Ruff, pytest, mypy configuration
├── requirements.txt                # Pinned production dependencies
├── requirements-dev.txt            # Dev/test dependencies
└── CONTRIBUTING.md                 # Contribution guidelines
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit 1.45, Plotly 5.24 |
| Data | Pandas 2.2, NumPy 1.26 |
| NLP | Custom 80+ skill taxonomy, compiled regex |
| ML | scikit-learn 1.5 (GradientBoostingRegressor, R²=0.93) |
| Testing | pytest + pytest-cov (50 tests) |
| Linting | ruff |
| CI/CD | GitHub Actions (lint → test → Docker build) |
| Deployment | Docker (multi-stage, non-root) |
| Logging | Rotating file + console, structured format |

## Docker

```bash
docker build -t gjmip .
docker run -p 8501:8501 gjmip
```

## Development

```bash
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=nlp --cov=models --cov=utils

# Lint
ruff check .

# Format
ruff format .
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

## License

[MIT](LICENSE)

---

<div align="center">

**Built by [Arin Pattnaik](https://github.com/ArinPattnaik)**

[🌐 Live Demo](https://global-job-market-intelligence-platform-arin.streamlit.app/) · [⭐ Star on GitHub](https://github.com/ArinPattnaik/global-job-market-intelligence-platform)

</div>
