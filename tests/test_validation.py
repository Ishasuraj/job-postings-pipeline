from src.clean import validate_row


def test_validate_row_accepts_valid_row():
    row = {
        "title": "Data Analyst",
        "location": "Remote",
        "fraudulent": 0,
        "salary_range": "$90,000 - $110,000",
    }

    assert validate_row(row) is True


def test_validate_row_rejects_missing_title():
    row = {
        "title": "",
        "location": "Remote",
        "fraudulent": 0,
    }

    assert validate_row(row) is False


def test_validate_row_rejects_missing_location():
    row = {
        "title": "Data Analyst",
        "location": "",
        "fraudulent": 0,
    }

    assert validate_row(row) is False


def test_validate_row_rejects_invalid_fraudulent_value():
    row = {
        "title": "Data Analyst",
        "location": "Remote",
        "fraudulent": 2,
    }

    assert validate_row(row) is False


def test_validate_row_rejects_bad_salary_format():
    row = {
        "title": "Data Analyst",
        "location": "Remote",
        "fraudulent": 0,
        "salary_range": "not a salary",
    }

    assert validate_row(row) is False
