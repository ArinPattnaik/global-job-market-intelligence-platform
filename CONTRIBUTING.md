# Contributing

Thanks for your interest in contributing to the Global Job Market Intelligence Platform.

## Development Setup

```bash
# Clone and enter the project
git clone https://github.com/ArinPattnaik/global-job-market-intelligence-platform.git
cd global-job-market-intelligence-platform

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dev dependencies
pip install -r requirements-dev.txt

# Generate sample data
python data/generate_synthetic_data.py

# Run the app
streamlit run app.py
```

## Code Quality

We use **ruff** for linting and formatting, and **pytest** for testing.

```bash
# Lint
ruff check .

# Format
ruff format .

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=nlp --cov=models --cov=utils --cov-report=term-missing
```

## Project Structure

| Directory | Purpose |
|-----------|---------|
| `config/` | Settings, logging configuration |
| `utils/`  | Shared utilities (data loading, chart helpers, UI components) |
| `nlp/`    | Skill extraction taxonomy and NLP pipeline |
| `models/` | ML model training and prediction |
| `etl/`    | API data fetching |
| `pages/`  | Streamlit dashboard pages |
| `tests/`  | Test suite |
| `data/`   | Raw and processed datasets |
| `assets/` | CSS and static files |

## Pull Request Guidelines

1. Create a feature branch from `main`
2. Ensure all tests pass (`pytest tests/ -v`)
3. Ensure code passes linting (`ruff check .`)
4. Write tests for new functionality
5. Keep PRs focused — one feature or fix per PR
