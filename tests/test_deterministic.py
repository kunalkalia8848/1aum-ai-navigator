import pytest
from modules.readiness import calculate_readiness_scores, maturity_level
from modules.prioritization import (
    calculate_priority_score,
    classify_use_case,
    normalize_name
)
from modules.risk_register import calculate_risk_score, classify_risk
from modules.roadmap import generate_conditional_actions


# ==========================================
# READINESS TESTS
# ==========================================
def test_readiness_empty_responses():
    with pytest.raises(ValueError, match="At least one readiness response is required."):
        calculate_readiness_scores([])

def test_readiness_correct_averages_and_maturity():
    responses = [
        {"category": "Strategy & Executive Alignment", "question_id": "Q1", "score": 4},
        {"category": "Strategy & Executive Alignment", "question_id": "Q2", "score": 4},
        {"category": "Data & Infrastructure", "question_id": "Q3", "score": 2},
        {"category": "Data & Infrastructure", "question_id": "Q4", "score": 2},
    ]
    scores = calculate_readiness_scores(responses)
    assert scores["category_scores"]["Strategy & Executive Alignment"] == 4.0
    assert scores["category_scores"]["Data & Infrastructure"] == 2.0
    assert scores["overall_score"] == 3.0

def test_readiness_maturity_level_thresholds():
    assert maturity_level(1.2) == "Ad Hoc"
    assert maturity_level(2.8) == "Emerging"
    assert maturity_level(3.8) == "Developing"
    assert maturity_level(4.8) == "Leading"


# ==========================================
# PRIORITIZATION TESTS
# ==========================================
def test_prioritization_min_and_max_scores():
    min_score = calculate_priority_score(
        impact=1, feasibility=1, risk=5, alignment=1, data_readiness=1
    )
    max_score = calculate_priority_score(
        impact=5, feasibility=5, risk=1, alignment=5, data_readiness=5
    )
    assert min_score < max_score

def test_prioritization_risk_inversion():
    low_risk = calculate_priority_score(
        impact=4, feasibility=4, risk=1, alignment=4, data_readiness=4
    )
    high_risk = calculate_priority_score(
        impact=4, feasibility=4, risk=5, alignment=4, data_readiness=4
    )
    assert low_risk > high_risk

def test_prioritization_classification():
    # Expects (impact, feasibility, alignment, data_readiness, risk)
    quick_win = classify_use_case(5, 5, 5, 5, 1)
    strategic = classify_use_case(5, 2, 5, 2, 2)
    long_term = classify_use_case(2, 2, 2, 2, 4)
    
    assert isinstance(quick_win, str)
    assert isinstance(strategic, str)
    assert isinstance(long_term, str)

def test_prioritization_name_normalization():
    assert normalize_name("  Customer  Support AI ") == "customer support ai"


# ==========================================
# RISK REGISTER TESTS
# ==========================================
def test_risk_score_calculation():
    score = calculate_risk_score(likelihood=4, impact=5)
    assert score == 20

def test_risk_severity_classification():
    assert classify_risk(20) == "Critical"
    assert classify_risk(12) == "High"
    assert classify_risk(6) == "Medium"
    assert classify_risk(2) == "Low"


# ==========================================
# ROADMAP TESTS
# ==========================================
def test_roadmap_conditional_gap_triggers():
    readiness_results = {
        "category_scores": {
            "Data & Infrastructure": 2.0,
            "Governance & Risk Management": 2.0,
            "Talent & Deployment Capability": 2.0
        }
    }
    risk_register = [{"severity": "Critical"}]
    selected_use_case = {"name": "Test Case"}
    
    actions = generate_conditional_actions(readiness_results, risk_register, selected_use_case)
    assert isinstance(actions, list)
# ==========================================
# STEP 59: BOUNDARY VALUE TESTS
# ==========================================
def test_risk_classification_boundaries():
    assert classify_risk(5) == "Low"
    assert classify_risk(6) == "Medium"
    assert classify_risk(11) == "Medium"
    assert classify_risk(12) == "High"
    assert classify_risk(19) == "High"
    assert classify_risk(20) == "Critical"
    assert classify_risk(25) == "Critical"


def test_maturity_level_boundaries():
    assert maturity_level(1.99) == "Ad Hoc"
    assert maturity_level(2.00) == "Emerging"
    assert maturity_level(2.99) == "Emerging"
    assert maturity_level(3.00) == "Developing"
    assert maturity_level(3.99) == "Developing"
    assert maturity_level(4.00) == "Established"
    assert maturity_level(4.49) == "Established"
    assert maturity_level(4.50) == "Leading"