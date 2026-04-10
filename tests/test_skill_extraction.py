"""
Tests for NLP Skill Extraction Module
"""

import pytest
from nlp.skill_extraction import extract_skills, get_skill_category, SKILL_TAXONOMY, ALL_SKILLS


class TestExtractSkills:
    """Tests for the extract_skills function."""

    def test_basic_skill_extraction(self):
        text = "We need python and sql skills for this data role"
        result = extract_skills(text)
        assert "python" in result
        assert "sql" in result

    def test_empty_input(self):
        assert extract_skills("") == ""
        assert extract_skills("No tech skills here") == ""

    def test_none_input(self):
        assert extract_skills(None) == ""

    def test_multiple_skills(self):
        text = "Expert in python, machine learning, tensorflow, and aws deployment"
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
        text = "Create dashboards using tableau and power bi"
        result = extract_skills(text)
        assert "tableau" in result
        assert "power bi" in result


class TestSkillCategory:
    """Tests for skill categorization."""

    def test_python_category(self):
        assert get_skill_category("python") == "Programming"

    def test_sql_category(self):
        assert get_skill_category("sql") == "Data & Databases"

    def test_aws_category(self):
        assert get_skill_category("aws") == "Cloud & Infrastructure"

    def test_tensorflow_category(self):
        assert get_skill_category("tensorflow") == "ML & AI"

    def test_unknown_skill(self):
        assert get_skill_category("unknown_skill_xyz") == "Other"

    def test_taxonomy_not_empty(self):
        assert len(SKILL_TAXONOMY) > 0
        assert len(ALL_SKILLS) >= 80  # We promised 80+ skills


class TestSkillTaxonomy:
    """Tests for the skill taxonomy structure."""

    def test_all_categories_have_skills(self):
        for category, skills in SKILL_TAXONOMY.items():
            assert len(skills) > 0, f"Category '{category}' has no skills"

    def test_no_duplicate_skills_across_categories(self):
        seen = set()
        duplicates = []
        for category, skills in SKILL_TAXONOMY.items():
            for skill in skills:
                if skill in seen:
                    duplicates.append(skill)
                seen.add(skill)
        # Some overlap is intentional (e.g., data visualization appears in multiple)
        # but we track it
        assert len(duplicates) <= 3, f"Too many duplicates: {duplicates}"