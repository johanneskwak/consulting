import streamlit as st
import random

# ==========================================
# 1. 초기 상태 세팅 (st.session_state)
# ==========================================
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.scene = 'lobby' # 'lobby', 'game', 'ending'
    
    # 메타 프로그레션 (누적 재화 및 영구 인벤토리)
    st.session_state.global_money = 1000 
    st.session_state.global_cards = ['마케터'] 
    
    # 게임 내 상태
    st.session_state.turn = 1
    st.session_state.hp = 150
    st.session_state.mp = 50
    st.session_state.logs = []
    st.session_state.active_event = None
    
    # 사장님 고집 (보스전 기믹)
    st.session_state.ceo_blocking = False
    st.session_state.pending_solution = None
    
    # 회사 5대 지표 (A회사 예시)
    st.session_state.stats = {
        'product': 85, 'employee': 30, 'product_aware': 60, 
        'brand_aware': 70, 'profit': 20
    }

# ==========================================
# 2. 게임 코어 함수
# ==========================================
def add_log(msg):
    st.session_state.logs.insert(0, f"[턴 {st.session_state.turn}] {msg}")

def pass_turn(hp_cost, mp_cost):
    if st.session_state.turn >= 20 or st.session_state.hp <= 0:
        st.session_state.scene = 'ending'
        return
        
    st.session_state.hp -= (hp_cost + 10) # 기본 유지비 10
    st.session_state.mp = min(100, st.session_state.mp - mp_cost + 15) # MP 회복
    st.session_state.turn += 1
    
    # 돌발 악재 발생 (15% 확률)
    if random.random() < 0.15 and not st.session_state.active_event:
        st.session_state.active_event = {'name': '특허 분쟁', 'penalty': 30, 'target_card': '변리사'}
        add_log("🚨 [돌발 악재] 타사의 특허 침해 소송이 들어왔습니다!")

def execute_solution(choice):
    # 딜레마 선택지 처리
    st.session_state.pending_solution = choice
    st.session_state.ceo_blocking = True # 사장님이 일단 반대함
    add_log(f"솔루션 '{choice}'을(를) 제안했습니다. 사장님을 설득해야 합니다!")

def persuade_ceo(method):
    st.session_state.ceo_blocking = False
    choice = st.session_state.pending_solution
    
    if method == 'card' and '변호사' in st.session_state.global_cards:
        add_log("🛡️ 변호사 카드로 법적 타당성을 증명하여 사장님을 완벽히 설득했습니다!")
        pass_turn(0, 0)
    elif method == 'mp':
        add_log("🗣️ 열띤 프레젠테이션으로 사장님을 설득했습니다. (MP -30)")
        st.session_state.mp -= 30
        pass_turn(0, 0)
    else:
        add_log("❌ 설득에 실패했습니다. 솔루션이 반려되고 턴만 소모되었습니다.")
        pass_turn(0, 0)
        return

    # 딜레마 결과 적용
    if choice == 'A안 (안정형)':
        st.session_state.stats['employee'] += 10
        st.session_state.stats['profit'] += 10
        add_log("직무 재배치를 안정적으로 완료했습니다. 지표가 소폭 상승합니다.")
    elif choice == 'B안 (정석형)':
        st.session_state.hp -= 30
        st.session_state.stats['employee'] += 30
        st.session_state.stats['profit'] += 20
        add_log("외부 강사를 초빙해 대대적인 재교육을 실시했습니다. 비용이 들었지만 지표가 크게 오릅니다.")
    elif choice == 'C안 (극약처방)':
        st.session_state.stats['employee'] = 10
        st.session_state.stats['profit'] = 100
        add_log("대규모 구조조정을 단행했습니다! 수익성은 극대화되었으나 직원들의 불만이 폭발합니다.")

# ==========================================
# 3. 화면 렌더링: 로비 (네트워킹 & 성장)
# ==========================================
if st.session_state.scene == 'lobby':
    st.title("🏢 내 컨설팅 펌 (로비)")
    st.markdown("성공적인 컨설팅으로 번 돈으로 인맥을 넓히고 회사를 키우세요.")
    st.metric("보유 자본금", f"{st.session_state.global_money} 만원")
    
    st.subheader("🤝 네트워킹 파티 (직업 스카우트)")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**변호사 영입 (비용: 500만원)**\n\n법적 분쟁 악재를 방어하고, 고집불통 사장님을 논리로 제압합니다.")
        if st.button("변호사 스카우트"):
            if st.session_state.global_money >= 500 and '변호사' not in st.session_state.global_cards:
                st.session_state.global_money -= 500
                st.session_state.global_cards.append('변호사')
                st.rerun()
    with col2:
        st.info("**변리사 영입 (비용: 400만원)**\n\n특허 관련 소송을 전면 방어하여 회사의 현금 유출을 막습니다.")
        if st.button("변리사 스카우트"):
            if st.session_state.global_money >= 400 and '변리사' not in st.session_state.global_cards:
                st.session_state.global_money -= 400
                st.session_state.global_cards.append('변리사')
                st.rerun()
                
    st.write(f"**현재 보유 인맥:** {', '.join(st.session_state.global_cards)}")
    
    st.divider()
    if st.button("🚀 A회사 컨설팅 시작하기", use_container_width=True):
        st.session_state.scene = 'game'
        # 게임 초기화
        st.session_state.turn = 1
        st.session_state.hp = 150
        st.session_state.mp = 50
        st.session_state.logs = []
        st.session_state.ceo_blocking = False
        st.session_state.stats = {'product': 85, 'employee': 30, 'product_aware': 60, 'brand_aware': 70, 'profit': 20}
        st.rerun()

# ==========================================
# 4. 화면 렌더링: 게임 플레이
# ==========================================
elif st.session_state.scene == 'game':
    st.title("📊 Consulting Tycoon: A회사")
    
    # 상단 상태바
    col1, col2, col3 = st.columns(3)
    col1.metric("Turn", f"{st.session_state.turn} / 20")
    col2.metric("HP (유동성)", st.session_state.hp)
    col3.metric("MP (인사이트)", st.session_state.mp)
    
    st.divider()
    
    # 메인 레이아웃
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.subheader("📈 회사 5대 지표")
        stats = st.session_state.stats
        st.progress(stats['product']/100, text=f"상품 퀄리티 ({stats['product']})")
        st.progress(stats['employee']/100, text=f"직원 퀄리티 ({stats['employee']})")
        st.progress(stats['product_aware']/100, text=f"상품 인지도 ({stats['product_aware']})")
        st.progress(stats['brand_aware']/100, text=f"브랜드 인지도 ({stats['brand_aware']})")
        st.progress(stats['profit']/100, text=f"돈 버는 능력 ({stats['profit']})")
        
        st.subheader("📰 Market News (단서)")
        st.info("[블라인드 썰] 우리 회사 일하는 사람만 일한다... 효율 최악임")
        
        # 사장님 고집 기믹
        if st.session_state.ceo_blocking:
            st.error("🤬 사장님: '우리 회사는 원래 이렇게 해왔어! 이 방식은 너무 위험해!'")
            if st.button("🗣️ 논리로 설득하기 (MP 30 소모)"):
                if st.session_state.mp >= 30: persuade_ceo('mp')
                st.rerun()
            if '변호사' in st.session_state.global_cards:
                if st.button("🛡️ 변호사 카드 사용 (법적 타당성 증명)"):
                    persuade_ceo('card')
                    st.rerun()
                    
        # 액션 및 딜레마 패널
        elif not st.session_state.ceo_blocking:
            st.subheader("⚡ 액션 (솔루션 딜레마)")
            st.write("문제 원인을 파악했다면, 어떤 솔루션을 실행하시겠습니까?")
            if st.button("A안: 부서 이동만 지시 (비용 0, 효과 미미)", use_container_width=True):
                execute_solution('A안 (안정형)')
                st.rerun()
            if st.button("B안: 외부 컨설팅 및 대대적 재교육 (HP -30, 효과 확실)", use_container_width=True):
                execute_solution('B안 (정석형)')
                st.rerun()
            if st.button("C안: 절반 해고 및 수익 몰빵 (직원 퀄리티 파괴, 수익성 100)", use_container_width=True):
                execute_solution('C안 (극약처방)')
                st.rerun()

    with right_col:
        st.subheader("🎒 내 인벤토리")
        for card in st.session_state.global_cards:
            st.success(f"💳 {card} 카드")
            
        if st.session_state.active_event:
            event = st.session_state.active_event
            st.error(f"{event['name']} 발생! (-{event['penalty']} HP)")
            if event['target_card'] in st.session_state.global_cards:
                if st.button(f"{event['target_card']}로 방어!"):
                    add_log(f"{event['target_card']} 카드로 악재를 완벽히 막았습니다!")
                    st.session_state.active_event = None
                    st.rerun()
            if st.button("몸으로 때우기 (HP 감소)"):
                st.session_state.hp -= event['penalty']
                add_log("악재를 막지 못해 현금이 유출되었습니다.")
                st.session_state.active_event = None
                st.rerun()
                
        st.subheader("📝 진행 로그")
        for log in st.session_state.logs[:5]: # 최근 5개만 표시
            st.caption(log)

# ==========================================
# 5. 화면 렌더링: 멀티 엔딩
# ==========================================
elif st.session_state.scene == 'ending':
    st.title("🏁 컨설팅 종료 (결과 보고서)")
    stats = st.session_state.stats
    
    if st.session_state.hp <= 0:
        st.error("자금 고갈로 회사가 파산했습니다. 컨설팅 실패!")
        st.session_state.global_money += 100 # 실패 위로금
    else:
        # 5대 지표 기반 멀티 엔딩 판별
        if stats['profit'] >= 80 and stats['employee'] <= 30:
            st.warning("📺 [뉴스] A회사, 흑자 전환 성공... 그러나 '최악의 직장' 오명으로 줄퇴사 이어져")
            st.session_state.global_money += 500
        elif stats['profit'] >= 60 and stats['employee'] >= 60:
            st.success("📺 [뉴스] A회사, 직원 만족과 수익성 두 마리 토끼를 다 잡은 유니콘 기업으로 도약!")
            st.balloons()
            st.session_state.global_money += 1500
        else:
            st.info("📺 [뉴스] A회사, 현상 유지는 했으나 뚜렷한 성장 동력은 보이지 않아...")
            st.session_state.global_money += 300
            
    if st.button("로비로 돌아가기"):
        st.session_state.scene = 'lobby'
        st.rerun()