# SQL Query Results

## Query 1
```sql
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
ORDER BY fraud_rate_pct DESC
```

| employment_type   |   total_postings |   fraud_count |   fraud_rate_pct |
|:------------------|-----------------:|--------------:|-----------------:|
| part-time         |              783 |            74 |             9.45 |
| other             |              219 |            15 |             6.85 |
| full-time         |            11524 |           485 |             4.21 |
| contract          |             1512 |            42 |             2.78 |
| temporary         |              239 |             2 |             0.84 |

## Query 2
```sql
-- 2. Fraud rate by required experience level
SELECT
    required_experience,
    COUNT(*) AS total_postings,
    SUM(fraudulent) AS fraud_count,
    ROUND(100.0 * SUM(fraudulent) / COUNT(*), 2) AS fraud_rate_pct
FROM job_postings
WHERE required_experience != ''
GROUP BY required_experience
ORDER BY fraud_rate_pct DESC
```

| required_experience   |   total_postings |   fraud_count |   fraud_rate_pct |
|:----------------------|-----------------:|--------------:|-----------------:|
| entry level           |             2685 |           177 |             6.59 |
| executive             |              140 |             9 |             6.43 |
| not applicable        |             1100 |            60 |             5.45 |
| director              |              386 |            17 |             4.4  |
| mid-senior level      |             3776 |           113 |             2.99 |
| internship            |              368 |            10 |             2.72 |
| associate             |             2282 |            41 |             1.8  |

## Query 3
```sql
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
LIMIT 10
```

| industry                            |   total_postings |   fraud_count |   fraud_rate_pct |
|:------------------------------------|-----------------:|--------------:|-----------------:|
| Information Technology and Services |             1718 |            32 |             1.86 |
| Computer Software                   |             1364 |             5 |             0.37 |
| Internet                            |             1048 |             0 |             0    |
| Education Management                |              822 |             0 |             0    |
| Marketing and Advertising           |              821 |            45 |             5.48 |
| Financial Services                  |              774 |            34 |             4.39 |
| Hospital & Health Care              |              495 |            50 |            10.1  |
| Consumer Services                   |              357 |            24 |             6.72 |
| Telecommunications                  |              340 |            25 |             7.35 |
| Oil & Energy                        |              285 |           107 |            37.54 |

## Query 4
```sql
-- 4. Does having a company logo correlate with fraud?
SELECT
    has_company_logo,
    COUNT(*) AS total_postings,
    SUM(fraudulent) AS fraud_count,
    ROUND(100.0 * SUM(fraudulent) / COUNT(*), 2) AS fraud_rate_pct
FROM job_postings
GROUP BY has_company_logo
```

|   has_company_logo |   total_postings |   fraud_count |   fraud_rate_pct |
|-------------------:|-----------------:|--------------:|-----------------:|
|                  0 |             3605 |           568 |            15.76 |
|                  1 |            13929 |           279 |             2    |

## Query 5
```sql
-- 5. Telecommuting vs fraud rate
SELECT
    telecommuting,
    COUNT(*) AS total_postings,
    SUM(fraudulent) AS fraud_count,
    ROUND(100.0 * SUM(fraudulent) / COUNT(*), 2) AS fraud_rate_pct
FROM job_postings
GROUP BY telecommuting
```

|   telecommuting |   total_postings |   fraud_count |   fraud_rate_pct |
|----------------:|-----------------:|--------------:|-----------------:|
|               0 |            16788 |           784 |             4.67 |
|               1 |              746 |            63 |             8.45 |

## Query 6
```sql
-- 6. Overall fraud rate + total postings (single summary row)
SELECT
    COUNT(*) AS total_postings,
    SUM(fraudulent) AS total_fraud,
    ROUND(100.0 * SUM(fraudulent) / COUNT(*), 2) AS overall_fraud_rate_pct
FROM job_postings
```

|   total_postings |   total_fraud |   overall_fraud_rate_pct |
|-----------------:|--------------:|-------------------------:|
|            17534 |           847 |                     4.83 |

## Query 7
```sql
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
LIMIT 10
```

| industry                     |   total_postings |   fraud_rate_pct |   fraud_rank |
|:-----------------------------|-----------------:|-----------------:|-------------:|
| Oil & Energy                 |              285 |            37.54 |            1 |
| Accounting                   |              159 |            35.85 |            2 |
| Leisure, Travel & Tourism    |               75 |            28    |            3 |
| Hospitality                  |               86 |            13.95 |            4 |
| Real Estate                  |              174 |            13.79 |            5 |
| Health, Wellness and Fitness |              125 |            12    |            6 |
| Hospital & Health Care       |              495 |            10.1  |            7 |
| Telecommunications           |              340 |             7.35 |            8 |
| Entertainment                |               74 |             6.76 |            9 |
| Consumer Services            |              357 |             6.72 |           10 |
