
# Global Job Market Intelligence Platform

An advanced end-to-end Data Analytics platform that aggregates job postings globally and analyzes hiring trends.

## Features
- Job ingestion via Adzuna API
- ETL data pipeline
- NLP skill extraction
- Salary prediction ML model
- Interactive Streamlit dashboard
- Global hiring analytics
- Job search interface

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your Adzuna API credentials
6. Run the ETL pipeline: `python scripts/update_pipeline.py`
7. Train the model: `python models/train_model.py`
8. Run the app: `streamlit run app.py`

## Run Locally

Install dependencies

```bash
pip install -r requirements.txt
```

Fetch jobs

```bash
python etl/fetch_jobs.py
```

Extract skills

```bash
python nlp/skill_extraction.py
```

Train salary model

```bash
python models/train_model.py
```

Run dashboard

```bash
streamlit run app.py
```

## Deployment

### Docker

Build and run with Docker:

```bash
docker build -t job-platform .
docker run -p 8501:8501 job-platform
```

### Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Set main file path to `app.py`
5. Add secrets for `ADZUNA_APP_ID` and `ADZUNA_APP_KEY`

## Project Structure

- `app.py`: Main Streamlit application
- `config/settings.py`: Configuration settings
- `etl/fetch_jobs.py`: Job data fetching script
- `nlp/skill_extraction.py`: Skill extraction from job descriptions
- `models/train_model.py`: Salary prediction model training
- `pages/`: Streamlit multi-page components
- `scripts/update_pipeline.py`: Pipeline update script
- `data/`: Data storage (raw and processed)
- `logs/`: Application logs
- `requirements.txt`: Python dependencies
- `Dockerfile`: Docker configuration
- `.env.example`: Environment variables template

## Architecture

API → ETL Pipeline → Dataset → NLP → ML Model → Dashboard
