import streamlit as st
import random

# ==========================================
# 1. 시나리오 데이터 (다양한 직무 및 외부 재앙)
# ==========================================
SCENARIOS = [
    {
        "domain": "HR (인사/조직)",
        "news": "📰 [블라인드 썰] 우리 회사 일하는 사람만 일한다... 부서 이기주의 심각.",
        "choices": {
            "A안": {"text": "부서 통폐합 지시 (비용 0 / MP 10)", "hp": 0, "mp": 10, "stats": {"employee": 10, "profit": 5}},
            "B안": {"text": "외부 조직문화 컨설팅 (HP 20)", "hp": 20, "mp": 0, "stats": {"employee": 25, "profit": -5}},
            "C안": {"text": "대규모 구조조정 단행 (MP 20)", "hp": 0, "mp": 20, "stats": {"employee": -20, "profit": 30}}
        }
    },
    {
        "domain": "Marketing (마케팅/영업)",
        "news": "📰 [시장 동향] 신제품 스펙은 압도적인데, 소비자들은 존재조차 모른다?",
        "choices": {
            "A안": {"text": "SNS 바이럴 마케팅 (HP 10 / MP 10)", "hp": 10, "mp": 10, "stats": {"product_aware": 20, "brand_aware": 10}},
            "B안": {"text": "대규모 TV/옥외 광고 (HP 40)", "hp": 40, "mp": 0, "stats": {"product_aware": 40, "brand_aware": 20}},
            "C안": {"text": "초특가 할인 판매 (수익성 악화)", "hp": 0, "mp": 10, "stats": {"product_aware": 15, "profit": -20}}
        }
    },
    {
        "domain": "External (외부 재앙/공급망)",
        "news": "📰 [속보] 주요 원자재 생산국 대지진 발생! 물류 마비로 원가 폭등 우려.",
        "choices": {
            "A안": {"text": "대체 공급선 긴급 발굴 (MP 30)", "hp": 0, "mp": 30, "stats": {"product": -10, "profit": 15}},
            "B안": {"text": "프리미엄 라인업 한정 생산 (HP 20)", "hp": 20, "mp": 10, "stats": {"product": 15, "profit": -10}},
            "C안": {"text": "공장 가동 일시 중단 (피해 감수)", "hp": 15, "mp": 0, "stats": {"brand_aware": -10, "profit": -15}}
        }
    },
    {
        "domain": "R&D (제품/품질)",
        "news": "📰 [테크 리뷰] '디자인만 예쁘고 잔고장이 너무 많아요.' 소비자 불만 폭주.",
        "choices": {
            "A안": {"text": "R&D 예산 긴급 증액 (HP 30)", "hp": 30, "mp": 0, "stats": {"product": 30, "profit": -10}},
            "B안": {"text": "무상 A/S 기간 전격 연장 (HP 20)", "hp": 20, "mp": 10, "stats": {"brand_aware": 25, "profit": -15}},
            "C안": {"text": "리뷰 삭제 알바 고용 (편법/위험)", "hp": 5, "mp": 10, "stats": {"product_aware": -10, "brand_aware": -20}}
        }
    }
]

# ==========================================
# 2. 초기 상태 세팅 (st.session_state)
# ==========================================
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.scene = 'lobby'
    st.session_state.global_money = 1000 
    st.session_state.global_cards = ['마케터'] 
    
    st.session_state.turn = 1
    st.session_state.hp = 100
    st.session_state.mp = 50
    st.session_state.logs = []
    
    st.session_state.ceo_blocking = False
    st.session_state.pending_solution = None
    st.session_state.current_scenario = random.choice(SCENARIOS) # 첫 시나리오 할당
    
    st.session_state.stats = {
        'product': 50, 'employee': 50, 'product_aware': 50, 
        'brand_aware': 50, 'profit': 50
    }

# ==========================================
# 3. 게임 코어 함수
# ==========================================
def add_log(msg):
    st.session_state.logs.insert(0, f"[턴 {st.session_state.turn}] {msg}")

def pass_turn():
    # 1. 턴 당 기본 회복 로직 (+5)
    st.session_state.hp = max(0, st.session_state.hp + 5)
    st.session_state.mp = min(100, max(0, st.session_state.mp + 5))
    
    st.session_state.turn += 1
    
    # 2. 게임 오버 / 클리어 체크
    if st.session_state.hp <= 0 or st.session_state.turn > 20:
        st.session_state.scene = 'ending'
        return
        
    # 3. 다음 턴을 위한 새로운 랜덤 시나리오 배정
    st.session_state.current_scenario = random.choice(SCENARIOS)
    st.session_state.ceo_blocking = False
    st.session_state.pending_solution = None
    add_log(f"턴 종료. (HP/MP 5 회복) 새로운 위기가 발생했습니다.")

def apply_solution_effects(choice_key):
    # 선택한 솔루션의 비용과 효과를 적용
    scenario = st.session_state.current_scenario
    effect = scenario['choices'][choice_key]
    
    # 비용 차감 (마이너스 방지)
    st.session_state.hp = max(0, st.session_state.hp - effect['hp'])
    st.session_state.mp = max(0, st.session_state.mp - effect['mp'])
    
    # 지표 변동 (0~100 사이 유지)
    for stat_key, value in effect['stats'].items():
        current_stat = st.session_state.stats[stat_key]
        st.session_state.stats[stat_key] = min(100, max(0, current_stat + value))
        
    add_log(f"'{effect['text']}' 실행 완료!")

def persuade_ceo(method):
    st.session_state.ceo_blocking = False
    choice_key = st.session_state.pending_solution
    
    # 설득 비용 처리
    if method == 'card':
        add_log("🛡️ 변호사 카드로 완벽히 설득했습니다!")
    elif method == 'mp':
        if st.session_state.mp < 30:
            add_log("❌ MP가 부족하여 설득에 실패했습니다.")
            pass_turn()
            return
        st.session_state.mp -= 30
        add_log("🗣️ 열띤 프레젠테이션으로 사장님을 설득했습니다. (MP -30)")
    else:
        add_log("❌ 설득을 포기했습니다.")
        pass_turn()
        return

    # 설득 성공 시 효과 적용 후 턴 넘김
    apply_solution_effects(choice_key)
    pass_turn()

# ==========================================
# 4. 화면 렌더링: 로비
# ==========================================
if st.session_state.scene == 'lobby':
    st.title("🏢 내 컨설팅 펌 (로비)")
    st.metric("보유 자본금", f"{st.session_state.global_money} 만원")
    
    st.subheader("🤝 네트워킹 파티 (직업 스카우트)")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**변호사 영입 (500만원)**\n\n고집불통 사장님을 논리로 제압합니다.")
        if st.button("변호사 스카우트"):
            if st.session_state.global_money >= 500 and '변호사' not in st.session_state.global_cards:
                st.session_state.global_money -= 500
                st.session_state.global_cards.append('변호사')
                st.rerun()
    with col2:
        st.info("**변리사 영입 (400만원)**\n\n특허 관련 소송을 전면 방어합니다.")
        if st.button("변리사 스카우트"):
            if st.session_state.global_money >= 400 and '변리사' not in st.session_state.global_cards:
                st.session_state.global_money -= 400
                st.session_state.global_cards.append('변리사')
                st.rerun()
                
    st.write(f"**현재 보유 인맥:** {', '.join(st.session_state.global_cards)}")
    
    if st.button("🚀 종합 기업 컨설팅 시작하기", use_container_width=True):
        st.session_state.scene = 'game'
        st.session_state.turn = 1
        st.session_state.hp = 100
        st.session_state.mp = 50
        st.session_state.logs = []
        st.session_state.ceo_blocking = False
        st.session_state.stats = {'product': 50, 'employee': 50, 'product_aware': 50, 'brand_aware': 50, 'profit': 50}
        st.session_state.current_scenario = random.choice(SCENARIOS)
        st.rerun()

# ==========================================
# 5. 화면 렌더링: 게임 플레이
# ==========================================
elif st.session_state.scene == 'game':
    st.title("📊 Consulting Tycoon")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("⏳ Turn", f"{st.session_state.turn} / 20")
    col2.metric("💰 HP (유동성)", st.session_state.hp)
    col3.metric("🧠 MP (인사이트)", st.session_state.mp)
    
    st.divider()
    
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.subheader("📈 회사 5대 지표")
        stats = st.session_state.stats
        st.progress(stats['product']/100, text=f"상품 퀄리티 ({stats['product']})")
        st.progress(stats['employee']/100, text=f"직원 퀄리티 ({stats['employee']})")
        st.progress(stats['product_aware']/100, text=f"상품 인지도 ({stats['product_aware']})")
        st.progress(stats['brand_aware']/100, text=f"브랜드 인지도 ({stats['brand_aware']})")
        st.progress(stats['profit']/100, text=f"돈 버는 능력 ({stats['profit']})")
        
        # 다이내믹 시나리오 렌더링
        scenario = st.session_state.current_scenario
        st.subheader(f"⚠️ 현재 당면한 과제: {scenario['domain']}")
        st.info(scenario['news'])
        
        if st.session_state.ceo_blocking:
            st.error("🤬 사장님: '그 방식은 너무 위험해! 반대일세!'")
            if st.button("🗣️ 논리로 설득하기 (MP 30 소모)"):
                persuade_ceo('mp')
                st.rerun()
            if '변호사' in st.session_state.global_cards:
                if st.button("🛡️ 변호사 카드 사용 (비용 없이 즉시 통과)"):
                    persuade_ceo('card')
                    st.rerun()
            if st.button("설득 포기 (턴만 소모)"):
                persuade_ceo('give_up')
                st.rerun()
                
        else:
            st.subheader("⚡ 컨설팅 솔루션 제안")
            choices = scenario['choices']
            
            # A, B, C 다이내믹 버튼 생성
            for key, choice_data in choices.items():
                if st.button(f"{key}: {choice_data['text']}", use_container_width=True):
                    # 자원 부족 체크
                    if st.session_state.hp < choice_data['hp']:
                        st.warning("자금(HP)이 부족합니다!")
                    elif st.session_state.mp < choice_data['mp']:
                        st.warning("행동력(MP)이 부족합니다!")
                    else:
                        st.session_state.pending_solution = key
                        st.session_state.ceo_blocking = True
                        add_log(f"솔루션 '{key}'을(를) 제안했습니다. 사장님을 설득하세요!")
                        st.rerun()

    with right_col:
        st.subheader("🎒 내 인벤토리")
        for card in st.session_state.global_cards:
            st.success(f"💳 {card} 카드")
                
        st.subheader("📝 진행 로그")
        for log in st.session_state.logs[:6]:
            st.caption(log)

# ==========================================
# 6. 화면 렌더링: 멀티 엔딩
# ==========================================
elif st.session_state.scene == 'ending':
    st.title("🏁 컨설팅 최종 결과 보고서")
    stats = st.session_state.stats
    
    if st.session_state.hp <= 0:
        st.error("💸 자금이 완전히 고갈되어 회사가 파산했습니다. (Game Over)")
    else:
        avg_stat = sum(stats.values()) / 5
        if avg_stat >= 70:
            st.success("🌟 [뉴스] 컨설팅 대성공! 회사가 업계 1위의 유니콘 기업으로 성장했습니다!")
            st.balloons()
            st.session_state.global_money += 1500
        elif avg_stat >= 40:
            st.warning("📺 [뉴스] 위기는 넘겼으나 뚜렷한 성장 동력은 보이지 않아...")
            st.session_state.global_money += 500
        else:
            st.error("📉 [뉴스] 최악의 컨설팅으로 회사 지표가 엉망이 되었습니다.")
            
    if st.button("로비로 돌아가기"):
        st.session_state.scene = 'lobby'
        st.rerun()
