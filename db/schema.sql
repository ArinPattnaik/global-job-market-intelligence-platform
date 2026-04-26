-- ============================================================
-- Global Job Market Intelligence Platform — Database Schema
-- ============================================================
-- PostgreSQL-compatible schema with proper constraints,
-- indexes, and audit columns.
-- ============================================================

CREATE TABLE IF NOT EXISTS jobs (
    id              SERIAL PRIMARY KEY,
    job_id          VARCHAR(20) UNIQUE NOT NULL,
    title           TEXT NOT NULL,
    category        VARCHAR(100),
    seniority       VARCHAR(50),
    company         VARCHAR(255),
    city            VARCHAR(255),
    country         VARCHAR(10) NOT NULL,
    country_name    VARCHAR(100),
    location        TEXT,
    salary_min      INTEGER CHECK (salary_min >= 0),
    salary_max      INTEGER CHECK (salary_max >= salary_min),
    salary_avg      INTEGER GENERATED ALWAYS AS ((salary_min + salary_max) / 2) STORED,
    description     TEXT,
    skills          TEXT,
    job_type        VARCHAR(50),
    experience_years INTEGER CHECK (experience_years >= 0),
    posted_date     DATE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ── Indexes ─────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_jobs_country ON jobs (country);
CREATE INDEX IF NOT EXISTS idx_jobs_category ON jobs (category);
CREATE INDEX IF NOT EXISTS idx_jobs_seniority ON jobs (seniority);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs (company);
CREATE INDEX IF NOT EXISTS idx_jobs_posted_date ON jobs (posted_date DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_salary_avg ON jobs (salary_avg);
CREATE INDEX IF NOT EXISTS idx_jobs_job_type ON jobs (job_type);

-- Full-text search index on description
CREATE INDEX IF NOT EXISTS idx_jobs_description_fts
    ON jobs USING GIN (to_tsvector('english', COALESCE(description, '')));

-- ── Audit trigger ───────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_jobs_updated_at ON jobs;
CREATE TRIGGER trg_jobs_updated_at
    BEFORE UPDATE ON jobs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
