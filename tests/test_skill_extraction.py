import pytest
from nlp.skill_extraction import extract_skills

def test_extract_skills():
    text = "We need python and sql skills"
    result = extract_skills(text)
    assert "python" in result
    assert "sql" in result
    assert "excel" not in result

def test_extract_skills_empty():
    text = "No skills here"
    result = extract_skills(text)
    assert result == ""