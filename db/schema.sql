
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    country TEXT,
    salary_min INT,
    salary_max INT,
    description TEXT,
    skills TEXT,
    posted_date DATE
);
