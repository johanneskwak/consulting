import streamlit as st
import random

# ==========================================
# 1. 시나리오 및 랜덤 미션 데이터
# ==========================================
MISSIONS = [
    {"id": "brand", "name": "✨ 명품 브랜드의 탄생", "desc": "우리 브랜드를 하이엔드 명품으로 만드세요. (조건: 브랜드 인지도 95 이상, 상품 퀄리티 90 이상)", "reward": 2000},
    {"id": "hr", "name": "🏢 꿈의 직장", "desc": "모두가 입사하고 싶어하는 최고의 직장을 만드세요. (조건: 직원 퀄리티 95 이상, 돈 버는 능력 50 이상 유지)", "reward": 1500},
    {"id": "profit", "name": "💰 캐시카우", "desc": "압도적인 현금 창출 능력을 증명하세요. (조건: 돈 버는 능력 95 이상, 최종 HP 200 이상)", "reward": 2000},
    {"id": "awareness", "name": "🛒 국민 아이템", "desc": "전 국민이 아는 메가 히트 상품을 만드세요. (조건: 상품 인지도 95 이상, 상품 퀄리티 80 이상)", "reward": 1500},
    {"id": "balanced", "name": "🦄 육각형 유니콘", "desc": "모든 지표가 우수한 밸런스형 기업으로 성장시키세요. (조건: 5대 지표 평균 75점 이상)", "reward": 3000}
]

# 카드 효과 및 다양한 직무 시나리오
SCENARIOS = [
    {
        "domain": "Finance (재무/세금)",
        "news": "📰 [경제] 국세청, 당사에 대한 전격 특별 세무조사 착수! 추징금 40 HP 예상.",
        "card_solvers": {
            "회계사": {
                "desc": "추징금 50% 방어", 
                "text": "정밀한 회계 감사를 통해 세금 폭탄을 절반으로 줄였습니다! (HP -20 방어 성공)", 
                "hp_cost": 20, "stats": {"profit": 10}
            },
            "세무사": {
                "desc": "추징금 30% 방어", 
                "text": "세무 조정을 통해 추징금의 일부를 방어했습니다! (HP -28로 선방)", 
                "hp_cost": 28, "stats": {"profit": 5}
            }
        },
        "choices": {
            "A안": {"text": "조사에 성실히 임하며 과징금 전액 납부 (HP 40)", "hp": 40, "mp": 0, "stats": {"profit": -15}},
            "B안": {"text": "재무팀 풀가동으로 소명 자료 완벽 준비 (MP 30)", "hp": 0, "mp": 30, "stats": {"employee": -15, "profit": 5}},
            "C안": {"text": "언론 플레이로 국세청 압박 (위험/브랜드 타격)", "hp": 0, "mp": 10, "stats": {"brand_aware": -20, "profit": -10}}
        }
    },
    {
        "domain": "HR (인사/조직)",
        "news": "📰 [블라인드 썰] '일하는 사람만 일한다' 부서 간 이기주의 심각, 핵심 인재 퇴사 줄이어...",
        "card_solvers": {
            "노무사": {
                "desc": "인사 위기 완벽 해결", 
                "text": "노사 갈등을 원만하게 중재하고 불만 사항을 합법적으로 해결했습니다! (비용 0)", 
                "hp_cost": 0, "stats": {"employee": 20}
            }
        },
        "choices": {
            "A안": {"text": "전사적 워크샵 및 소통 강화 (HP 15)", "hp": 15, "mp": 0, "stats": {"employee": 15, "profit": -5}},
            "B안": {"text": "인사평가 시스템 전면 개편 (MP 20)", "hp": 0, "mp": 20, "stats": {"employee": 10, "profit": 10}},
            "C안": {"text": "성과 미달자 권고사직 (극약처방)", "hp": 0, "mp": 10, "stats": {"employee": -15, "profit": 25}}
        }
    },
    {
        "domain": "Legal (법무/소송)",
        "news": "📰 [법률 속보] 경쟁사에서 100억 원대 특허 침해 및 영업방해 소송 전격 제기!",
        "card_solvers": {
            "변호사": {
                "desc": "소송 완벽 방어", 
                "text": "철저한 법리 검토로 소송을 기각시키고 오히려 합의금을 받아냈습니다! (비용 0)", 
                "hp_cost": 0, "stats": {"profit": 15, "brand_aware": 10}
            }
        },
        "choices": {
            "A안": {"text": "거액의 합의금 지불 후 조기 종결 (HP 40)", "hp": 40, "mp": 0, "stats": {"profit": -10, "brand_aware": -5}},
            "B안": {"text": "자체 법무팀 야근으로 맞소송 준비 (MP 30)", "hp": 0, "mp": 30, "stats": {"employee": -10, "brand_aware": 5}},
            "C안": {"text": "무대응으로 일관 (패소 위험)", "hp": 20, "mp": 0, "stats": {"profit": -20, "brand_aware": -15}}
        }
    },
    {
        "domain": "Production (제조/품질)",
        "news": "📰 [소비자 고발] 주력 상품에서 유해물질 검출 논란! 전량 리콜 위기.",
        "choices": {
            "A안": {"text": "전량 리콜 및 조건 없는 환불 (HP 40)", "hp": 40, "mp": 0, "stats": {"brand_aware": 15, "profit": -20}},
            "B안": {"text": "기준치 이하라고 과학적 데이터로 반박 (MP 30)", "hp": 0, "mp": 30, "stats": {"brand_aware": -15, "product": 10}},
            "C안": {"text": "해당 라인만 조용히 단종 (HP 15)", "hp": 15, "mp": 0, "stats": {"product": -15, "profit": 5}}
        }
    },
    {
        "domain": "Sales (영업/B2B)",
        "news": "📰 [업계 동향] 회사의 최대 납품처, 돌연 파산 선고. 대금 회수 불투명 및 연쇄 부도 우려.",
        "choices": {
            "A안": {"text": "긴급 자금 대출로 연쇄 부도 방어 (HP 30)", "hp": 30, "mp": 0, "stats": {"profit": -15, "brand_aware": 5}},
            "B안": {"text": "영업팀 총동원하여 신규 거래처 긴급 발굴 (MP 30)", "hp": 0, "mp": 30, "stats": {"product_aware": 15, "employee": -10}},
            "C안": {"text": "미수금 포기하고 사내 긴축 재정 돌입 (HP 10)", "hp": 10, "mp": 0, "stats": {"profit": 15, "employee": -15}}
        }
    },
    {
        "domain": "Competitor (경쟁사)",
        "news": "📰 [스타트업] 파격적인 반값 가격표를 단 카피캣 제품 등장! 시장 점유율 폭락 중.",
        "choices": {
            "A안": {"text": "출혈 경쟁 불사! 맞불 초특가 할인 (HP 30)", "hp": 30, "mp": 0, "stats": {"profit": -25, "product_aware": 20}},
            "B안": {"text": "디자인 및 성능 개선 프리미엄 전략 (MP 30)", "hp": 0, "mp": 30, "stats": {"brand_aware": 15, "product": 15}},
            "C안": {"text": "기존 충성 고객 대상 멤버십 혜택 강화 (HP 15 / MP 10)", "hp": 15, "mp": 10, "stats": {"profit": -5, "brand_aware": 10}}
        }
    },
    {
        "domain": "Marketing (마케팅/영업)",
        "news": "📰 [시장 동향] 신제품 퀄리티는 역대급인데, 소비자 인지도가 0%에 수렴 중...",
        "choices": {
            "A안": {"text": "타겟 맞춤형 SNS 바이럴 캠페인 (HP 10 / MP 10)", "hp": 10, "mp": 10, "stats": {"product_aware": 20, "profit": 5}},
            "B안": {"text": "유명 연예인 발탁 대규모 TV 광고 (HP 40)", "hp": 40, "mp": 0, "stats": {"product_aware": 40, "brand_aware": 20, "profit": -10}},
            "C안": {"text": "재고 떨이 반값 할인 (브랜드 타격)", "hp": 0, "mp": 10, "stats": {"product_aware": 15, "brand_aware": -10, "profit": -15}}
        }
    },
    {
        "domain": "External (외부 재앙/공급망)",
        "news": "📰 [속보] 주요 부품 생산국에 대규모 홍수 발생! 공급망 마비로 원자재가 폭등.",
        "choices": {
            "A안": {"text": "단가 높은 대체 공급선 긴급 계약 (HP 25)", "hp": 25, "mp": 0, "stats": {"product": 5, "profit": -15}},
            "B안": {"text": "사태 진정까지 공장 가동 축소 (MP 20)", "hp": 0, "mp": 20, "stats": {"product_aware": -10, "profit": -10}},
            "C안": {"text": "품질이 낮은 저가 부품으로 일시 대체 (위험)", "hp": 0, "mp": 10, "stats": {"product": -20, "profit": 15, "brand_aware": -15}}
        }
    }
]

# ==========================================
# 2. 초기 상태 세팅
# ==========================================
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.scene = 'lobby'
    st.session_state.global_money = 1000 
    st.session_state.card_charges = {} 
    st.session_state.current_mission = None
    
    st.session_state.turn = 1
    st.session_state.hp = 100
    st.session_state.mp = 50
    st.session_state.logs = []
    
    st.session_state.ceo_blocking = False
    st.session_state.pending_solution = None
    st.session_state.current_scenario = random.choice(SCENARIOS) 
    
    st.session_state.stats = {
        'product': 50, 'employee': 50, 'product_aware': 50, 
        'brand_aware': 50, 'profit': 50
    }

# ==========================================
# 3. 게임 코어 함수
# ==========================================
def add_log(msg):
    st.session_state.logs.insert(0, f"[턴 {st.session_state.turn}] {msg}")

def pick_new_scenario():
    new_scenario = random.choice(SCENARIOS)
    while new_scenario['domain'] == st.session_state.current_scenario['domain']:
        new_scenario = random.choice(SCENARIOS)
    return new_scenario

def pass_turn():
    # 매턴 HP와 MP 10씩 회복으로 상향 조정
    st.session_state.hp = max(0, st.session_state.hp + 10)
    st.session_state.mp = min(100, max(0, st.session_state.mp + 10))
    
    st.session_state.turn += 1
    
    if st.session_state.hp <= 0 or st.session_state.turn > 20:
        st.session_state.scene = 'ending'
        return
        
    st.session_state.current_scenario = pick_new_scenario()
    st.session_state.ceo_blocking = False
    st.session_state.pending_solution = None
    add_log(f"턴 종료. (HP/MP 10 자동 회복) 새로운 위기가 보고되었습니다.")

def apply_solution_effects(choice_key):
    scenario = st.session_state.current_scenario
    effect = scenario['choices'][choice_key]
    
    st.session_state.hp = max(0, st.session_state.hp - effect['hp'])
    st.session_state.mp = max(0, st.session_state.mp - effect['mp'])
    
    for stat_key, value in effect['stats'].items():
        st.session_state.stats[stat_key] = min(100, max(0, st.session_state.stats[stat_key] + value))
        
    add_log(f"솔루션 '{choice_key}' 실행 완료!")

# ==========================================
# 4. 화면 렌더링: 로비
# ==========================================
if st.session_state.scene == 'lobby':
    st.title("🏢 내 컨설팅 펌 (로비)")
    
    with st.expander("🏆 게임 목표 및 승리 조건 (필독)", expanded=True):
        st.markdown("""
        **1. 목표 하달:** 게임 시작 시 클라이언트가 원하는 **구체적인 목표(미션)**가 무작위로 주어집니다.
        **2. 전략적 선택:** 20턴 동안 파산을 막으며 목표 조건을 달성하세요. 매 턴 HP/MP가 10씩 회복됩니다.
        **3. 파산 주의:** 위기가 닥쳤을 때 실행할 수 있는 선택지가 하나도 없으면 **즉시 파산(게임 오버)**합니다.
        **4. 직업 카드 방어:** 특정 위기 발생 시 인벤토리의 카드를 사용해 즉시 해결하거나 피해를 줄이세요.
        """)
        
    st.metric("보유 자본금 (수임료)", f"{st.session_state.global_money} 만원")
    
    st.subheader("🤝 네트워킹 파티 (직업 스카우트)")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.info("**변호사 (500만)**\n\n법무/소송 완벽 방어\n**(최대 5회)**")
        if st.button("영입", key="btn_law"):
            if st.session_state.global_money >= 500 and '변호사' not in st.session_state.card_charges:
                st.session_state.global_money -= 500
                st.session_state.card_charges['변호사'] = 5
                st.rerun()
    with c2:
        st.info("**노무사 (300만)**\n\n인사/HR 완벽 방어\n**(최대 3회)**")
        if st.button("영입", key="btn_hr"):
            if st.session_state.global_money >= 300 and '노무사' not in st.session_state.card_charges:
                st.session_state.global_money -= 300
                st.session_state.card_charges['노무사'] = 3
                st.rerun()
    with c3:
        st.info("**회계사 (400만)**\n\n재무/세금 비용 50% 방어\n**(최대 3회)**")
        if st.button("영입", key="btn_acc"):
            if st.session_state.global_money >= 400 and '회계사' not in st.session_state.card_charges:
                st.session_state.global_money -= 400
                st.session_state.card_charges['회계사'] = 3
                st.rerun()
    with c4:
        st.info("**세무사 (200만)**\n\n재무/세금 비용 30% 방어\n**(최대 3회)**")
        if st.button("영입", key="btn_tax"):
            if st.session_state.global_money >= 200 and '세무사' not in st.session_state.card_charges:
                st.session_state.global_money -= 200
                st.session_state.card_charges['세무사'] = 3
                st.rerun()
                
    if st.session_state.card_charges:
        st.write("**현재 보유 인맥:**")
        cols = st.columns(len(st.session_state.card_charges))
        for i, (card, charges) in enumerate(st.session_state.card_charges.items()):
            cols[i].success(f"💳 {card} ({charges}회)")
    else:
        st.write("보유 중인 직업 카드가 없습니다.")
    
    st.divider()
    if st.button("🚀 무작위 미션 배정받고 컨설팅 시작하기", use_container_width=True, type="primary"):
        st.session_state.scene = 'game'
        st.session_state.turn = 1
        st.session_state.hp = 100
        st.session_state.mp = 50
        st.session_state.current_mission = random.choice(MISSIONS) 
        st.session_state.logs = [f"이번 컨설팅 목표: {st.session_state.current_mission['name']}"]
        st.session_state.ceo_blocking = False
        st.session_state.stats = {'product': 50, 'employee': 50, 'product_aware': 50, 'brand_aware': 50, 'profit': 50}
        st.session_state.current_scenario = random.choice(SCENARIOS)
        st.rerun()

# ==========================================
# 5. 화면 렌더링: 게임 플레이
# ==========================================
elif st.session_state.scene == 'game':
    mission = st.session_state.current_mission
    st.title("📊 Consulting Tycoon")
    
    st.info(f"🎯 **[이번 게임의 목표] {mission['name']}**\n\n{mission['desc']}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("⏳ Turn", f"{st.session_state.turn} / 20")
    col2.metric("💰 HP (자금)", st.session_state.hp)
    col3.metric("🧠 MP (행동력)", st.session_state.mp)
    
    st.divider()
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.subheader("📈 회사 5대 지표")
        stats = st.session_state.stats
        st.progress(stats['product']/100, text=f"상품 퀄리티 ({stats['product']})")
        st.progress(stats['employee']/100, text=f"직원 만족도 ({stats['employee']})")
        st.progress(stats['product_aware']/100, text=f"상품 인지도 ({stats['product_aware']})")
        st.progress(stats['brand_aware']/100, text=f"브랜드 가치 ({stats['brand_aware']})")
        st.progress(stats['profit']/100, text=f"돈 버는 능력 ({stats['profit']})")
        
        scenario = st.session_state.current_scenario
        st.subheader(f"⚠️ 현재 당면한 과제: {scenario['domain']}")
        st.warning(scenario['news'])
        
        if st.session_state.ceo_blocking:
            st.error("🤬 사장님: '그 방식은 비용이나 리스크가 너무 커! 반대일세!'")
            if st.button("🗣️ 논리로 설득하기 (MP 20 소모)"):
                if st.session_state.mp < 20:
                    st.warning("행동력(MP)이 부족합니다!")
                else:
                    st.session_state.mp -= 20
                    st.session_state.ceo_blocking = False
                    add_log("프레젠테이션으로 사장님 설득에 성공했습니다!")
                    apply_solution_effects(st.session_state.pending_solution)
                    pass_turn()
                    st.rerun()
            if st.button("포기하고 턴 넘기기 (솔루션 무효)"):
                st.session_state.ceo_blocking = False
                add_log("설득을 포기했습니다.")
                pass_turn()
                st.rerun()
        else:
            # 다중 직업 카드 대응 로직
            card_solvers = scenario.get('card_solvers', {})
            for card_name, card_info in card_solvers.items():
                if card_name in st.session_state.card_charges and st.session_state.card_charges[card_name] > 0:
                    if st.button(f"🛡️ [{card_name} 사용] {card_info['desc']} (남은 횟수: {st.session_state.card_charges[card_name]}회)", type="primary"):
                        if st.session_state.hp < card_info['hp_cost']:
                            st.warning(f"카드를 써도 방어에 필요한 최소 자금({card_info['hp_cost']})이 부족합니다!")
                        else:
                            st.session_state.card_charges[card_name] -= 1
                            st.session_state.hp -= card_info['hp_cost']
                            
                            for stat_key, value in card_info['stats'].items():
                                st.session_state.stats[stat_key] = min(100, max(0, st.session_state.stats[stat_key] + value))
                            
                            add_log(f"[{card_name} 발동!] {card_info['text']}")
                            pass_turn()
                            st.rerun()
            
            st.subheader("⚡ 컨설팅 솔루션 제안")
            choices = scenario['choices']
            
            # 선택지 중 단 하나라도 실행 가능한지 확인하는 로직 (모두 불가능하면 강제 게임 오버)
            can_afford_any = False
            for key, choice_data in choices.items():
                if st.session_state.hp >= choice_data['hp'] and st.session_state.mp >= choice_data['mp']:
                    can_afford_any = True
                    break
            
            if not can_afford_any:
                st.error("🚨 자금(HP) 또는 행동력(MP)이 완전히 바닥나 더 이상 어떤 솔루션도 실행할 수 없습니다! 회사가 버티지 못합니다.")
                if st.button("파산 처리 (결과 보기)", use_container_width=True, type="primary"):
                    st.session_state.hp = 0  # 강제 파산
                    st.session_state.scene = 'ending'
                    st.rerun()
            else:
                for key, choice_data in choices.items():
                    # 버튼 비활성화 시각 효과를 위해 disabled 속성 활용
                    is_disabled = st.session_state.hp < choice_data['hp'] or st.session_state.mp < choice_data['mp']
                    btn_text = f"{key}: {choice_data['text']} (HP -{choice_data['hp']}, MP -{choice_data['mp']})"
                    
                    if st.button(btn_text, use_container_width=True, disabled=is_disabled):
                        if random.random() < 0.3:
                            st.session_state.pending_solution = key
                            st.session_state.ceo_blocking = True
                            add_log(f"솔루션 '{key}' 제안! 하지만 사장님이 강력히 반대합니다.")
                        else:
                            apply_solution_effects(key)
                            pass_turn()
                        st.rerun()

    with right_col:
        st.subheader("🎒 내 인벤토리")
        if not st.session_state.card_charges:
            st.write("보유 카드가 없습니다.")
        else:
            for card, charges in st.session_state.card_charges.items():
                st.success(f"💳 {card} ({charges}회)")
                
        st.subheader("📝 진행 로그")
        for log in st.session_state.logs[:6]:
            st.caption(log)

# ==========================================
# 6. 화면 렌더링: 엔딩
# ==========================================
elif st.session_state.scene == 'ending':
    st.title("🏁 컨설팅 최종 결과 보고서")
    mission = st.session_state.current_mission
    stats = st.session_state.stats
    
    st.subheader(f"부여된 미션: {mission['name']}")
    st.write(mission['desc'])
    st.divider()
    
    mission_success = False
    
    if st.session_state.hp <= 0:
        st.error("💸 자금이 완전히 고갈되어 회사가 파산했습니다. (게임 오버)")
    else:
        if mission['id'] == 'brand' and stats['brand_aware'] >= 95 and stats['product'] >= 90:
            mission_success = True
        elif mission['id'] == 'hr' and stats['employee'] >= 95 and stats['profit'] >= 50:
            mission_success = True
        elif mission['id'] == 'profit' and stats['profit'] >= 95 and st.session_state.hp >= 200:
            mission_success = True
        elif mission['id'] == 'awareness' and stats['product_aware'] >= 95 and stats['product'] >= 80:
            mission_success = True
        elif mission['id'] == 'balanced' and (sum(stats.values()) / 5) >= 75:
            mission_success = True

        st.write(f"최종 HP: {st.session_state.hp}")
        st.write("최종 5대 지표:")
        st.json(stats)
        
        if mission_success:
            st.success(f"🌟 [뉴스] 컨설팅 대성공! 클라이언트의 요구사항을 완벽히 달성했습니다.\n\n수임료 **{mission['reward']}만원**이 입금되었습니다.")
            st.balloons()
            st.session_state.global_money += mission['reward']
        else:
            st.error(f"📉 [뉴스] 파산은 면했지만, 클라이언트가 원했던 '{mission['name']}' 목표 달성에는 실패했습니다.\n\n위약금을 제외한 기본 수임료 300만원만 지급됩니다.")
            st.session_state.global_money += 300
            
    if st.button("로비로 돌아가기"):
        st.session_state.scene = 'lobby'
        st.rerun()
