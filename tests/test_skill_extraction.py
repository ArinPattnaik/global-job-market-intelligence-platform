"""
Tests for NLP Skill Extraction Module
========================================
Comprehensive tests covering extraction, categorization, and edge cases.
"""

import pytest

from nlp.skill_extraction import (
    ALL_SKILLS,
    SKILL_TAXONOMY,
    extract_skills,
    get_all_categories,
    get_skill_category,
)


class TestExtractSkills:
    """Tests for the extract_skills function."""

    def test_basic_skill_extraction(self):
        text = "We need python and sql skills for this data role"
        result = extract_skills(text)
        assert "python" in result
        assert "sql" in result

    def test_empty_input(self):
        assert extract_skills("") == ""

    def test_no_skills_found(self):
        assert extract_skills("No tech skills here at all") == ""

    def test_none_input(self):
        assert extract_skills(None) == ""

    def test_nan_input(self):
        assert extract_skills(float("nan")) == ""

    def test_numeric_input(self):
        assert extract_skills(12345) == ""

    def test_multiple_skills(self):
        text = "Expert in python, machine learning, tensorflow, and aws"
        result = extract_skills(text)
        skills = result.split(",")
        assert "python" in skills
        assert "machine learning" in skills
        assert "tensorflow" in skills
        assert "aws" in skills

    def test_case_insensitive(self):
        text = "Experience with Python, SQL, and AWS required"
        result = extract_skills(text)
        assert "python" in result
        assert "sql" in result
        assert "aws" in result

    def test_no_duplicates(self):
        text = "python python python skills in python"
        result = extract_skills(text)
        skills = result.split(",")
        assert skills.count("python") == 1

    def test_cloud_skills(self):
        text = "Deploy on aws, azure, or gcp with docker and kubernetes"
        result = extract_skills(text)
        skills = result.split(",")
        assert "aws" in skills
        assert "azure" in skills
        assert "gcp" in skills
        assert "docker" in skills
        assert "kubernetes" in skills

    def test_bi_skills(self):
        text = "Create dashboards in tableau and power bi for stakeholders"
        result = extract_skills(text)
        assert "tableau" in result
        assert "power bi" in result

    def test_short_skill_word_boundary(self):
        """Short skills like 'r' and 'go' should use word boundaries."""
        text = "We use R for statistical analysis"
        result = extract_skills(text)
        assert "r" in result.split(",")

    def test_short_skill_no_false_positive(self):
        """'r' should not match inside words like 'required'."""
        text = "This role is required for the team"
        result = extract_skills(text)
        assert "r" not in result.split(",")

    def test_multiword_skill(self):
        text = "Experience with machine learning and deep learning"
        result = extract_skills(text)
        assert "machine learning" in result
        assert "deep learning" in result

    def test_returns_comma_separated_string(self):
        text = "python sql aws"
        result = extract_skills(text)
        assert isinstance(result, str)
        skills = result.split(",")
        assert len(skills) >= 3


class TestGetSkillCategory:
    """Tests for the get_skill_category function."""

    def test_known_skill(self):
        assert get_skill_category("python") == "Programming"
        assert get_skill_category("sql") == "Data & Databases"
        assert get_skill_category("aws") == "Cloud & Infrastructure"

    def test_case_insensitive(self):
        assert get_skill_category("Python") == "Programming"
        assert get_skill_category("SQL") == "Data & Databases"

    def test_unknown_skill(self):
        assert get_skill_category("nonexistent_skill") == "Other"

    def test_whitespace_handling(self):
        assert get_skill_category("  python  ") == "Programming"


class TestTaxonomy:
    """Tests for the skill taxonomy structure."""

    def test_taxonomy_not_empty(self):
        assert len(SKILL_TAXONOMY) > 0

    def test_all_skills_mapped(self):
        for category, skills in SKILL_TAXONOMY.items():
            for skill in skills:
                assert skill in ALL_SKILLS
                assert ALL_SKILLS[skill] == category

    def test_get_all_categories(self):
        categories = get_all_categories()
        assert "Programming" in categories
        assert "ML & AI" in categories
        assert len(categories) == len(SKILL_TAXONOMY)

    def test_minimum_skill_count(self):
        """Taxonomy should have at least 80 skills."""
        assert len(ALL_SKILLS) >= 80
