from typing import List, Dict, Any

SENIOR_QUESTIONS = [
    {
        "id": "S1.1",
        "section": 1,
        "text": "농장의 주소를 입력해주세요.",
        "type": "text",
        "dimension": None,
        "order": 1
    },
    {
        "id": "S1.2",
        "section": 1,
        "text": "주로 재배하는 품목은 무엇인가요?",
        "type": "text",
        "dimension": None,
        "order": 2
    },
    {
        "id": "S1.3",
        "section": 1,
        "text": "농장 운영 기간은 총 몇 년이신가요?",
        "type": "number",
        "dimension": None,
        "order": 3
    },
    {
        "id": "S2.1",
        "section": 2,
        "text": "언제쯤 은퇴하고 농장을 넘겨주시길 희망하시나요?",
        "type": "choice",
        "options": ["1년 내", "1~3년 내", "3~5년 내", "정해지지 않음"],
        "dimension": None,
        "order": 4
    },
    {
        "id": "S2.2",
        "section": 2,
        "text": "농장을 승계할 때, 가장 중요하게 생각하는 것은 무엇인가요?",
        "type": "choice",
        "options": [
            "수익성 및 성장성",
            "계승 및 안정성",
            "사회적 가치",
            "거래의 신속성"
        ],
        "dimension": "philosophy",
        "scoring": {"수익성 및 성장성": 5, "계승 및 안정성": 2, "사회적 가치": 3, "거래의 신속성": 4},
        "order": 5
    },
    {
        "id": "S3.1",
        "section": 3,
        "text": "농장을 물려받을 사람이 어떤 목표를 가졌으면 하시나요?",
        "type": "choice",
        "options": [
            "현재의 안정적인 생산량을 꾸준히 유지했으면 한다",
            "새로운 기술을 도입해 생산량이나 매출을 더 늘렸으면 한다"
        ],
        "dimension": "business",
        "scoring": {"현재의 안정적인 생산량을 꾸준히 유지했으면 한다": 2, "새로운 기술을 도입해 생산량이나 매출을 더 늘렸으면 한다": 5},
        "order": 6
    },
    {
        "id": "S3.2",
        "section": 3,
        "text": "다음과 같은 두 명의 승계 희망자가 있다면, 누구와 먼저 대화를 시작하시겠습니까?",
        "type": "scenario",
        "options": [
            "[승계자 A] IT 전문가 출신, 스마트팜 기술로 생산성 2배 계획",
            "[승계자 B] 5년 경력, 전통 노하우 계승 희망"
        ],
        "dimension": "philosophy",
        "scoring": {"[승계자 A] IT 전문가 출신, 스마트팜 기술로 생산성 2배 계획": 5, "[승계자 B] 5년 경력, 전통 노하우 계승 희망": 2},
        "order": 7
    },
    {
        "id": "S3.3",
        "section": 3,
        "text": "승계가 완료된 후, 어떤 형태로든 농장과 관계를 이어가고 싶으신가요?",
        "type": "choice",
        "options": [
            "완전히 떠나고 싶다",
            "가끔 방문해서 조언해주고 싶다",
            "정기적인 자문역을 맡고 싶다"
        ],
        "dimension": "mentorship",
        "scoring": {"완전히 떠나고 싶다": 1, "가끔 방문해서 조언해주고 싶다": 3, "정기적인 자문역을 맡고 싶다": 5},
        "order": 8
    },
    {
        "id": "S4.1",
        "section": 4,
        "text": "농장 관련 상담 시, 주로 누구 또는 무엇을 이용하시나요? (2개 선택)",
        "type": "multi_choice",
        "options": [
            "지역 농협(NH농협은행) 지점 직원",
            "주변 농업인 동료",
            "자녀/가족",
            "스마트폰/인터넷"
        ],
        "dimension": None,
        "order": 9
    },
    {
        "id": "S4.2",
        "section": 4,
        "text": "은퇴 후 희망하는 소득 형태는 무엇인가요?",
        "type": "choice",
        "options": [
            "매각 대금을 일시에 받아 직접 관리하고 싶다",
            "농지연금처럼 매월 안정적인 금액을 평생 받고 싶다"
        ],
        "dimension": "finance",
        "scoring": {"매각 대금을 일시에 받아 직접 관리하고 싶다": 5, "농지연금처럼 매월 안정적인 금액을 평생 받고 싶다": 2},
        "order": 10
    }
]

YOUTH_QUESTIONS = [
    {
        "id": "Y1.1",
        "section": 1,
        "text": "희망하는 귀농 지역과 재배 품목은 무엇인가요?",
        "type": "text",
        "dimension": None,
        "order": 1
    },
    {
        "id": "Y1.2",
        "section": 1,
        "text": "농업 관련 경력이 있으신가요? (기간과 내용)",
        "type": "text",
        "dimension": None,
        "order": 2
    },
    {
        "id": "Y1.3",
        "section": 1,
        "text": "현재 확보 가능한 자기 자본 규모는 어느 정도인가요?",
        "type": "text",
        "dimension": None,
        "order": 3
    },
    {
        "id": "Y2.1",
        "section": 2,
        "text": "농장을 운영하게 된다면, 가장 중요하게 생각하는 가치는 무엇인가요?",
        "type": "choice",
        "options": [
            "수익성 및 성장성",
            "계승 및 안정성",
            "사회적 가치",
            "안정적 운영"
        ],
        "dimension": "philosophy",
        "scoring": {"수익성 및 성장성": 5, "계승 및 안정성": 2, "사회적 가치": 3, "안정적 운영": 2},
        "order": 4
    },
    {
        "id": "Y2.2",
        "section": 2,
        "text": "농장 인수 후 단기적인 목표는 무엇인가요?",
        "type": "choice",
        "options": [
            "우선 1~2년간은 기존 방식을 배우며 안정적으로 운영하는 것",
            "1년 내에 새로운 판로를 개척하거나 스마트팜 설비를 도입하여 매출을 끌어올리는 것"
        ],
        "dimension": "business",
        "scoring": {"우선 1~2년간은 기존 방식을 배우며 안정적으로 운영하는 것": 2, "1년 내에 새로운 판로를 개척하거나 스마트팜 설비를 도입하여 매출을 끌어올리는 것": 5},
        "order": 5
    },
    {
        "id": "Y3.1",
        "section": 3,
        "text": "기존에 농장을 운영하시던 분의 철학과 노하우를 어떻게 생각하시나요?",
        "type": "choice",
        "options": [
            "존중하지만, 사업 성공을 위해선 나의 새로운 방식이 더 중요하다고 생각한다",
            "수십 년의 경험은 돈으로 살 수 없는 자산이므로, 최대한 배우고 계승하고 싶다"
        ],
        "dimension": "philosophy",
        "scoring": {"존중하지만, 사업 성공을 위해선 나의 새로운 방식이 더 중요하다고 생각한다": 5, "수십 년의 경험은 돈으로 살 수 없는 자산이므로, 최대한 배우고 계승하고 싶다": 2},
        "order": 6
    },
    {
        "id": "Y3.2",
        "section": 3,
        "text": "성공적인 정착을 위해, 기존 농장주로부터 어떤 도움을 받고 싶으신가요?",
        "type": "choice",
        "options": [
            "인수인계 과정만 명확하면 충분하다",
            "정착 초기 몇 년간은 지속적인 조언과 도움이 필요하다",
            "동업자처럼 함께 논의하며 배우고 싶다"
        ],
        "dimension": "mentorship",
        "scoring": {"인수인계 과정만 명확하면 충분하다": 1, "정착 초기 몇 년간은 지속적인 조언과 도움이 필요하다": 3, "동업자처럼 함께 논의하며 배우고 싶다": 5},
        "order": 7
    },
    {
        "id": "Y4.1",
        "section": 4,
        "text": "귀농/승계 정보를 얻을 때, 가장 신뢰하는 채널은 무엇인가요? (2개 선택)",
        "type": "multi_choice",
        "options": [
            "정부/지자체 사이트",
            "온라인 커뮤니티/유튜브",
            "지역 농협/농업기술센터",
            "먼저 귀농한 선배/지인"
        ],
        "dimension": None,
        "order": 8
    },
    {
        "id": "Y4.2",
        "section": 4,
        "text": "농장 인수 자금 조달 시, 선호하는 방식은 무엇인가요?",
        "type": "choice",
        "options": [
            "자기 자본 비중을 높여 금융 부담을 최소화하고 싶다",
            "정책자금 등 레버리지를 적극 활용하여 더 큰 규모의 농장을 인수하고 싶다"
        ],
        "dimension": "finance",
        "scoring": {"자기 자본 비중을 높여 금융 부담을 최소화하고 싶다": 2, "정책자금 등 레버리지를 적극 활용하여 더 큰 규모의 농장을 인수하고 싶다": 5},
        "order": 9
    }
]


def get_questions_by_user_type(user_type: str) -> List[Dict[str, Any]]:
    if user_type.lower() == "senior":
        return SENIOR_QUESTIONS
    elif user_type.lower() == "youth":
        return YOUTH_QUESTIONS
    else:
        raise ValueError(f"Invalid user type: {user_type}")


def get_dimension_questions(user_type: str, dimension: str) -> List[Dict[str, Any]]:
    questions = get_questions_by_user_type(user_type)
    return [q for q in questions if q.get("dimension") == dimension]


def calculate_dimension_score(answers: List[Dict[str, Any]], dimension: str) -> float:
    dimension_answers = [a for a in answers if a.get("dimension") == dimension]
    if not dimension_answers:
        return 3.0
    
    total_score = sum(a.get("score", 3) for a in dimension_answers)
    return total_score / len(dimension_answers)