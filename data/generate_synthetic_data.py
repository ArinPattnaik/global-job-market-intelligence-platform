"""
Synthetic Job Market Data Generator
====================================
Generates 5,000+ realistic job postings across 8 countries for the
Global Job Market Intelligence Platform demo.

Usage:
    python data/generate_synthetic_data.py
"""

import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

random.seed(42)
np.random.seed(42)

# ── Country Configuration ────────────────────────────────────────────

COUNTRIES = {
    "us": {
        "name": "United States",
        "cities": ["New York", "San Francisco", "Seattle", "Austin", "Boston",
                    "Chicago", "Los Angeles", "Denver", "Washington DC", "Atlanta"],
        "salary_base": 125000,
    },
    "gb": {
        "name": "United Kingdom",
        "cities": ["London", "Manchester", "Edinburgh", "Birmingham", "Bristol",
                    "Cambridge", "Leeds", "Glasgow"],
        "salary_base": 72000,
    },
    "in": {
        "name": "India",
        "cities": ["Bangalore", "Mumbai", "Hyderabad", "Delhi NCR", "Pune",
                    "Chennai", "Kolkata", "Noida"],
        "salary_base": 18000,
    },
    "ca": {
        "name": "Canada",
        "cities": ["Toronto", "Vancouver", "Montreal", "Ottawa", "Calgary", "Waterloo"],
        "salary_base": 92000,
    },
    "au": {
        "name": "Australia",
        "cities": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        "salary_base": 98000,
    },
    "de": {
        "name": "Germany",
        "cities": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Stuttgart"],
        "salary_base": 70000,
    },
    "sg": {
        "name": "Singapore",
        "cities": ["Singapore"],
        "salary_base": 78000,
    },
    "fr": {
        "name": "France",
        "cities": ["Paris", "Lyon", "Toulouse", "Marseille", "Bordeaux"],
        "salary_base": 58000,
    },
}

COUNTRY_WEIGHTS = [0.28, 0.14, 0.14, 0.10, 0.08, 0.09, 0.08, 0.09]

# ── Job Roles ────────────────────────────────────────────────────────

ROLES = {
    "Data Scientist": {
        "weight": 0.18,
        "salary_mult": 1.15,
        "core_skills": ["python", "machine learning", "statistics", "deep learning", "pandas", "numpy", "scikit-learn"],
        "optional_skills": ["tensorflow", "pytorch", "r", "nlp", "computer vision", "a/b testing", "sql"],
    },
    "Data Analyst": {
        "weight": 0.20,
        "salary_mult": 0.85,
        "core_skills": ["sql", "excel", "python", "data visualization", "statistics"],
        "optional_skills": ["tableau", "power bi", "r", "pandas", "looker", "google analytics", "a/b testing"],
    },
    "Data Engineer": {
        "weight": 0.16,
        "salary_mult": 1.10,
        "core_skills": ["python", "sql", "spark", "airflow", "etl"],
        "optional_skills": ["kafka", "aws", "docker", "kubernetes", "dbt", "snowflake", "scala", "hadoop"],
    },
    "ML Engineer": {
        "weight": 0.12,
        "salary_mult": 1.25,
        "core_skills": ["python", "machine learning", "docker", "mlflow", "tensorflow"],
        "optional_skills": ["pytorch", "kubernetes", "aws", "gcp", "ci/cd", "fastapi", "spark"],
    },
    "Business Analyst": {
        "weight": 0.10,
        "salary_mult": 0.80,
        "core_skills": ["sql", "excel", "power bi", "data visualization", "requirements gathering"],
        "optional_skills": ["tableau", "jira", "python", "stakeholder management", "agile"],
    },
    "BI Developer": {
        "weight": 0.06,
        "salary_mult": 0.90,
        "core_skills": ["sql", "power bi", "tableau", "data modeling", "etl"],
        "optional_skills": ["python", "looker", "dax", "snowflake", "ssrs", "ssis"],
    },
    "Analytics Manager": {
        "weight": 0.04,
        "salary_mult": 1.35,
        "core_skills": ["sql", "python", "leadership", "stakeholder management", "data visualization"],
        "optional_skills": ["tableau", "power bi", "a/b testing", "strategy", "agile"],
    },
    "DevOps Engineer": {
        "weight": 0.05,
        "salary_mult": 1.10,
        "core_skills": ["docker", "kubernetes", "ci/cd", "linux", "terraform"],
        "optional_skills": ["aws", "azure", "gcp", "jenkins", "ansible", "python", "git"],
    },
    "AI Research Scientist": {
        "weight": 0.04,
        "salary_mult": 1.40,
        "core_skills": ["python", "deep learning", "pytorch", "nlp", "statistics"],
        "optional_skills": ["tensorflow", "computer vision", "reinforcement learning", "transformers", "llm", "research"],
    },
    "Cloud Engineer": {
        "weight": 0.05,
        "salary_mult": 1.05,
        "core_skills": ["aws", "docker", "kubernetes", "terraform", "linux"],
        "optional_skills": ["azure", "gcp", "python", "networking", "security", "ci/cd"],
    },
}

# ── Seniority Levels ────────────────────────────────────────────────

SENIORITY = {
    "Junior": {"factor": 0.65, "exp_range": (0, 2), "weight": 0.18},
    "Mid": {"factor": 0.88, "exp_range": (3, 5), "weight": 0.32},
    "Senior": {"factor": 1.18, "exp_range": (5, 9), "weight": 0.28},
    "Lead": {"factor": 1.50, "exp_range": (8, 14), "weight": 0.13},
    "Principal": {"factor": 1.85, "exp_range": (12, 22), "weight": 0.09},
}

# ── Job Types ────────────────────────────────────────────────────────

JOB_TYPES = {
    "Full-time": 0.62,
    "Remote": 0.20,
    "Contract": 0.10,
    "Hybrid": 0.06,
    "Part-time": 0.02,
}

# ── Companies ────────────────────────────────────────────────────────

COMPANIES = [
    # Big Tech
    "Google", "Microsoft", "Amazon", "Apple", "Meta", "Netflix", "Uber",
    "Salesforce", "Adobe", "Oracle", "IBM", "Intel", "Cisco", "VMware",
    # Fintech / Finance
    "JPMorgan Chase", "Goldman Sachs", "Morgan Stanley", "Stripe", "Square",
    "PayPal", "Bloomberg", "Capital One", "Revolut", "Wise",
    # Consulting
    "McKinsey", "BCG", "Deloitte", "Accenture", "PwC", "EY", "KPMG",
    # Data / Cloud
    "Snowflake", "Databricks", "Palantir", "Datadog", "Confluent",
    "MongoDB", "Elastic", "Cloudera", "Teradata",
    # AI / ML
    "OpenAI", "Anthropic", "DeepMind", "Hugging Face", "Scale AI",
    "DataRobot", "H2O.ai", "Weights & Biases",
    # E-commerce / Consumer
    "Shopify", "Instacart", "DoorDash", "Airbnb", "Spotify", "Pinterest",
    "Snap", "Reddit", "LinkedIn", "Twitter",
    # Healthcare
    "UnitedHealth", "Optum", "Cerner", "Epic Systems", "Moderna",
    # Startups
    "TechFlow AI", "DataSphere", "NeuralPath", "CloudMetrics", "QuantumLeap",
    "ByteScale", "InfoPulse", "CyberNova", "AlgoRithm Inc", "PixelForge",
    "StreamData", "CodeCraft", "VectorAI", "PredictHub", "GraphCore",
    "InsightIQ", "DeepAnalytics", "FlowState", "NexGen Data", "SmartPipe",
    "Cortex Labs", "Synthetix AI", "DataMesh Co", "PipelineIO", "InferAI",
]

# ── Description Templates ───────────────────────────────────────────

DESC_TEMPLATES = [
    "We are looking for a {seniority} {title} to join our {team} team. "
    "The ideal candidate will have strong expertise in {skills_str}. "
    "You will work on {project} and collaborate with cross-functional teams "
    "to drive data-driven decision making. {requirement}",

    "Join {company} as a {seniority} {title}! "
    "In this role, you'll leverage {skills_str} to {action}. "
    "We value individuals who are passionate about {domain} "
    "and can deliver impactful results. {requirement}",

    "{company} is seeking a talented {seniority} {title} to help us {goal}. "
    "You'll use {skills_str} to build scalable solutions. "
    "This role requires {exp_years}+ years of experience and a strong "
    "background in {domain}. {requirement}",

    "Exciting opportunity for a {seniority} {title} at {company}! "
    "We need someone with hands-on experience in {skills_str}. "
    "You will be responsible for {action} and mentoring junior team members. "
    "{requirement}",

    "As a {seniority} {title} at {company}, you will {action} using {skills_str}. "
    "This is a unique opportunity to work on cutting-edge {domain} projects "
    "in a fast-paced environment. {exp_years}+ years of relevant experience required. "
    "{requirement}",
]

TEAMS = ["analytics", "data science", "engineering", "machine learning",
         "platform", "growth", "product", "infrastructure", "research"]

PROJECTS = [
    "building ML pipelines at scale", "real-time data processing systems",
    "customer analytics and segmentation", "recommendation engines",
    "natural language processing solutions", "predictive modeling frameworks",
    "data warehouse modernization", "cloud migration projects",
    "business intelligence dashboards", "fraud detection systems",
    "supply chain optimization", "marketing attribution models",
]

ACTIONS = [
    "build and deploy production ML models",
    "design and implement data pipelines",
    "analyze complex datasets to uncover insights",
    "develop automated reporting solutions",
    "optimize our data infrastructure",
    "create interactive dashboards and visualizations",
    "implement statistical models for forecasting",
    "drive the adoption of data-driven culture",
    "architect scalable data solutions",
    "lead data science initiatives across the organization",
]

GOALS = [
    "scale our data platform", "transform how we use data",
    "build next-generation analytics", "revolutionize our data infrastructure",
    "drive innovation through data science", "modernize our analytics stack",
]

DOMAINS = [
    "data science", "machine learning", "analytics", "big data",
    "artificial intelligence", "business intelligence", "data engineering",
    "cloud computing", "statistical modeling",
]

REQUIREMENTS = [
    "Bachelor's or Master's degree in a quantitative field preferred.",
    "Strong communication skills and ability to present to stakeholders.",
    "Experience with agile methodologies is a plus.",
    "Competitive salary and comprehensive benefits package.",
    "Remote-friendly culture with flexible working hours.",
    "Opportunity for growth and professional development.",
    "Experience in a fast-paced startup environment is a plus.",
    "Strong problem-solving skills and attention to detail required.",
]


def weighted_choice(options: dict, key: str = "weight") -> str:
    """Pick a key from dict based on weights."""
    items = list(options.keys())
    weights = [options[k][key] if isinstance(options[k], dict) else options[k] for k in items]
    return random.choices(items, weights=weights, k=1)[0]


def generate_description(title, seniority, company, skills, exp_years):
    """Generate a realistic job description."""
    template = random.choice(DESC_TEMPLATES)
    skills_str = ", ".join(skills[:5])
    return template.format(
        title=title,
        seniority=seniority,
        company=company,
        skills_str=skills_str,
        team=random.choice(TEAMS),
        project=random.choice(PROJECTS),
        action=random.choice(ACTIONS),
        goal=random.choice(GOALS),
        domain=random.choice(DOMAINS),
        requirement=random.choice(REQUIREMENTS),
        exp_years=exp_years,
    )


def generate_jobs(n: int = 5000) -> pd.DataFrame:
    """Generate n synthetic job postings."""
    print(f"🔧 Generating {n} synthetic job postings...")
    jobs = []
    country_codes = list(COUNTRIES.keys())
    role_names = list(ROLES.keys())
    role_weights = [ROLES[r]["weight"] for r in role_names]
    seniority_names = list(SENIORITY.keys())
    seniority_weights = [SENIORITY[s]["weight"] for s in seniority_names]
    job_type_names = list(JOB_TYPES.keys())
    job_type_weights = list(JOB_TYPES.values())

    start_date = datetime.now() - timedelta(days=365)

    for i in range(n):
        # Pick country
        country_code = random.choices(country_codes, weights=COUNTRY_WEIGHTS, k=1)[0]
        country_info = COUNTRIES[country_code]

        # Pick role
        role = random.choices(role_names, weights=role_weights, k=1)[0]
        role_info = ROLES[role]

        # Pick seniority
        seniority = random.choices(seniority_names, weights=seniority_weights, k=1)[0]
        seniority_info = SENIORITY[seniority]

        # Generate salary
        base = country_info["salary_base"] * role_info["salary_mult"] * seniority_info["factor"]
        noise = np.random.normal(1.0, 0.12)
        salary_min = int(base * noise * 0.90)
        salary_max = int(base * noise * 1.15)
        salary_min = max(salary_min, 5000)
        salary_max = max(salary_max, salary_min + 2000)

        # Pick skills
        n_core = random.randint(2, min(4, len(role_info["core_skills"])))
        n_optional = random.randint(1, min(3, len(role_info["optional_skills"])))
        skills = random.sample(role_info["core_skills"], n_core) + \
                 random.sample(role_info["optional_skills"], n_optional)

        # Experience
        exp_years = random.randint(*seniority_info["exp_range"])

        # City
        city = random.choice(country_info["cities"])

        # Company
        company = random.choice(COMPANIES)

        # Job type
        job_type = random.choices(job_type_names, weights=job_type_weights, k=1)[0]

        # Date - slight recency bias
        days_ago = int(np.random.exponential(scale=90))
        days_ago = min(days_ago, 365)
        posted_date = start_date + timedelta(days=365 - days_ago)

        # Title with seniority prefix
        if seniority == "Junior":
            full_title = f"Junior {role}"
        elif seniority == "Lead":
            full_title = f"Lead {role}"
        elif seniority == "Principal":
            full_title = f"Principal {role}"
        else:
            full_title = f"{'Senior ' if seniority == 'Senior' else ''}{role}"

        # Description
        description = generate_description(role, seniority, company, skills, exp_years)

        jobs.append({
            "job_id": f"JOB-{i+1:05d}",
            "title": full_title,
            "category": role,
            "seniority": seniority,
            "company": company,
            "city": city,
            "country": country_code,
            "country_name": country_info["name"],
            "location": f"{city}, {country_info['name']}",
            "salary_min": salary_min,
            "salary_max": salary_max,
            "salary_avg": (salary_min + salary_max) // 2,
            "description": description,
            "skills": ",".join(skills),
            "job_type": job_type,
            "experience_years": exp_years,
            "posted_date": posted_date.strftime("%Y-%m-%d"),
        })

    df = pd.DataFrame(jobs)
    print(f"✅ Generated {len(df)} job records across {df['country_name'].nunique()} countries")
    print(f"   Roles: {df['category'].nunique()} | Companies: {df['company'].nunique()}")
    print(f"   Date range: {df['posted_date'].min()} → {df['posted_date'].max()}")
    return df


def main():
    # Setup paths
    base = Path(__file__).resolve().parent
    raw_dir = base / "raw"
    processed_dir = base / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Generate
    df = generate_jobs(5000)

    # Save raw
    raw_path = raw_dir / "jobs_raw.csv"
    df.to_csv(raw_path, index=False)
    print(f"💾 Raw data saved → {raw_path}")

    # Save processed (same data, skills already generated)
    processed_path = processed_dir / "jobs_processed.csv"
    df.to_csv(processed_path, index=False)
    print(f"💾 Processed data saved → {processed_path}")

    # Quick summary
    print("\n📊 Data Summary:")
    print(f"   Rows: {len(df)}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Countries: {df['country_name'].value_counts().to_dict()}")
    print(f"   Avg Salary: ${df['salary_avg'].mean():,.0f}")


if __name__ == "__main__":
    main()
