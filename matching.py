def calculate_match_score(donor_skill, request_skill):
    """
    재능기부자와 수요자의 재능 매칭 점수 계산
    
    Args:
        donor_skill: 재능기부자의 재능 (쉼표로 구분된 문자열)
        request_skill: 수요자가 필요한 재능
    
    Returns:
        int: 매칭 점수 (0 또는 1)
    """
    donor_skills = donor_skill.lower().split(",")
    request_skill = request_skill.lower()

    return 1 if any(s.strip() in request_skill for s in donor_skills) else 0

