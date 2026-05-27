from app.semantic_search import category_boost, concept_hits, semantic_score


def test_concept_hits_maps_related_terms() -> None:
    assert {"kubernetes", "crashloop"} <= concept_hits("AKS pod keeps dying")


def test_semantic_score_rewards_related_terms() -> None:
    score = semantic_score("pod keeps dying", "CrashLoopBackOff pod restart troubleshooting")
    assert score > 0


def test_category_boost_uses_focus_area() -> None:
    assert category_boost("terraform", "Terraform state drift plan apply") > 0
