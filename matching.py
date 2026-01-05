def calculate_match_score(donor_skill, request_skill):
    """
    재능기부자와 수요자의 재능 매칭 점수 계산 (Wild 매칭)
    
    Args:
        donor_skill: 재능기부자의 재능 (쉼표로 구분된 문자열)
        request_skill: 수요자가 필요한 재능
    
    Returns:
        int: 매칭 점수 (0 또는 1)
    """
    if not donor_skill or not request_skill:
        return 0
    
    donor_skills = [s.strip().lower() for s in donor_skill.split(",")]
    request_skill_lower = request_skill.lower()
    
    # 양방향 wild 매칭: 기부자 재능이 수요자 재능에 포함되거나, 수요자 재능이 기부자 재능에 포함되는 경우
    for skill in donor_skills:
        if skill and (skill in request_skill_lower or request_skill_lower in skill):
            return 1
    
    # 단어 단위 매칭: 각 단어가 부분적으로 일치하는지 확인
    request_words = request_skill_lower.split()
    for skill in donor_skills:
        if not skill:
            continue
        skill_words = skill.split()
        # 기부자 재능의 단어가 수요자 재능에 포함되거나, 수요자 재능의 단어가 기부자 재능에 포함되는 경우
        for skill_word in skill_words:
            if any(skill_word in req_word or req_word in skill_word for req_word in request_words):
                return 1
    
    return 0

