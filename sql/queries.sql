-- queries.sql
-- Analysis queries run against job_postings table in data/job_postings.db

-- 1. Fraud rate by employment type
SELECT
    employment_type,
    COUNT(*) AS total_postings,
    SUM(fraudulent) AS fraud_count,
    ROUND(100.0 * SUM(fraudulent) / COUNT(*), 2) AS fraud_rate_pct
FROM job_postings
WHERE employment_type != ''
GROUP BY employment_type
ORDER BY fraud_rate_pct DESC;


-- 2. Fraud rate by required experience level
SELECT
    required_experience,
    COUNT(*) AS total_postings,
    SUM(fraudulent) AS fraud_count,
    ROUND(100.0 * SUM(fraudulent) / COUNT(*), 2) AS fraud_rate_pct
FROM job_postings
WHERE required_experience != ''
GROUP BY required_experience
ORDER BY fraud_rate_pct DESC;


-- 3. Top 10 industries by posting volume, with their fraud rate
SELECT
    industry,
    COUNT(*) AS total_postings,
    SUM(fraudulent) AS fraud_count,
    ROUND(100.0 * SUM(fraudulent) / COUNT(*), 2) AS fraud_rate_pct
FROM job_postings
WHERE industry != ''
GROUP BY industry
ORDER BY total_postings DESC
LIMIT 10;


-- 4. Does having a company logo correlate with fraud?
SELECT
    has_company_logo,
    COUNT(*) AS total_postings,
    SUM(fraudulent) AS fraud_count,
    ROUND(100.0 * SUM(fraudulent) / COUNT(*), 2) AS fraud_rate_pct
FROM job_postings
GROUP BY has_company_logo;


-- 5. Telecommuting vs fraud rate
SELECT
    telecommuting,
    COUNT(*) AS total_postings,
    SUM(fraudulent) AS fraud_count,
    ROUND(100.0 * SUM(fraudulent) / COUNT(*), 2) AS fraud_rate_pct
FROM job_postings
GROUP BY telecommuting;


-- 6. Overall fraud rate + total postings (single summary row)
SELECT
    COUNT(*) AS total_postings,
    SUM(fraudulent) AS total_fraud,
    ROUND(100.0 * SUM(fraudulent) / COUNT(*), 2) AS overall_fraud_rate_pct
FROM job_postings;


-- 7. Ranking industries by fraud rate using a window function
-- (only industries with a meaningful sample size, >=50 postings)
SELECT
    industry,
    total_postings,
    fraud_rate_pct,
    RANK() OVER (ORDER BY fraud_rate_pct DESC) AS fraud_rank
FROM (
    SELECT
        industry,
        COUNT(*) AS total_postings,
        ROUND(100.0 * SUM(fraudulent) / COUNT(*), 2) AS fraud_rate_pct
    FROM job_postings
    WHERE industry != ''
    GROUP BY industry
    HAVING COUNT(*) >= 50
)
ORDER BY fraud_rank
LIMIT 10;