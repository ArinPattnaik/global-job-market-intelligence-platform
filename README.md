
# Global Job Market Intelligence Platform

An advanced end‑to‑end Data Analytics platform that aggregates job postings globally and analyzes hiring trends.

## Features
- Job ingestion via Adzuna API
- ETL data pipeline
- NLP skill extraction
- Salary prediction ML model
- Interactive Streamlit dashboard
- Global hiring analytics
- Job search interface

## Run Locally

Install dependencies

pip install -r requirements.txt

Fetch jobs

python etl/fetch_jobs.py

Extract skills

python nlp/skill_extraction.py

Train salary model

python models/train_model.py

Run dashboard

streamlit run app.py

## Architecture

API → ETL Pipeline → Database / Dataset → NLP → ML Model → Dashboard
