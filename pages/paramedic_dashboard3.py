import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import streamlit as st

# 각 대시보드 파일 상단에 추가
if st.sidebar.button("🏠 메인 화면으로"):
    st.switch_page("app.py")

# 페이지 설정
st.set_page_config(
    page_title="🚑 FIELD-DREAM 구급대원 대시보드",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링
st.markdown("""
<style>
    /* 전체 배경 및 폰트 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d3a 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 메인 타이틀 */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00d4ff 0%, #0066ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
    }
    
    /* 긴급 상태 카드 */
    .emergency-card {
        background: linear-gradient(135deg, #ff1744 0%, #d50000 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 2px solid #ff5252;
        box-shadow: 0 8px 32px rgba(255, 23, 68, 0.4);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 8px 32px rgba(255, 23, 68, 0.4); }
        50% { box-shadow: 0 8px 48px rgba(255, 23, 68, 0.8); }
    }
    
    /* AI 요약 카드 */
    .ai-summary {
        background: rgba(0, 212, 255, 0.1);
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 24px rgba(0, 212, 255, 0.3);
    }
    
    /* 네트워크 상태 표시 */
    .network-status {
        background: rgba(76, 175, 80, 0.15);
        border: 2px solid #4caf50;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .network-status.warning {
        background: rgba(255, 152, 0, 0.15);
        border-color: #ff9800;
    }
    
    .network-status.critical {
        background: rgba(244, 67, 54, 0.15);
        border-color: #f44336;
    }
    
    /* 병원 카드 */
    .hospital-card {
        background: linear-gradient(135deg, rgba(25, 118, 210, 0.2) 0%, rgba(13, 71, 161, 0.2) 100%);
        border: 2px solid #1976d2;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .hospital-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(25, 118, 210, 0.5);
        border-color: #00d4ff;
    }
    
    /* 메트릭 라벨 */
    .metric-label {
        font-size: 0.9rem;
        color: #90caf9;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #00d4ff;
        margin: 5px 0;
    }
    
    /* 실시간 처치 가이드 */
    .treatment-guide {
        background: rgba(156, 39, 176, 0.15);
        border-left: 4px solid #9c27b0;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
    }
    
    .priority-high {
        color: #ff5252;
        font-weight: 700;
    }
    
    .priority-medium {
        color: #ffb74d;
        font-weight: 600;
    }
    
    .priority-low {
        color: #81c784;
        font-weight: 500;
    }
    
    /* 로그 스타일 */
    .network-log {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 8px;
        padding: 10px;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        color: #4caf50;
        max-height: 200px;
        overflow-y: auto;
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        background: linear-gradient(135deg, #00d4ff 0%, #0066ff 100%);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'selected_hospital' not in st.session_state:
    st.session_state.selected_hospital = None
if 'emergency_start_time' not in st.session_state:
    st.session_state.emergency_start_time = datetime.now()

# 헤더
st.markdown('<h1 class="main-title">🚑 FIELD-DREAM 구급대원 대시보드</h1>', unsafe_allow_html=True)

# 현재 시간 및 경과 시간
current_time = datetime.now()
elapsed_time = current_time - st.session_state.emergency_start_time
col_time1, col_time2, col_time3 = st.columns(3)

with col_time1:
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="metric-label">현재 시각</div>
        <div class="metric-value">{current_time.strftime('%H:%M:%S')}</div>
    </div>
    """, unsafe_allow_html=True)

with col_time2:
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="metric-label">출동 경과 시간</div>
        <div class="metric-value" style="color: #ff5252;">{int(elapsed_time.total_seconds() // 60)}분 {int(elapsed_time.total_seconds() % 60)}초</div>
    </div>
    """, unsafe_allow_html=True)

with col_time3:
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="metric-label">사건 번호</div>
        <div class="metric-value" style="font-size: 1.5rem;">EMG-2025-0203-{np.random.randint(1000, 9999)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 메인 레이아웃: 좌측(상황 정보), 우측(병원 정보)
col_left, col_right = st.columns([1, 1])

with col_left:
    # 긴급 상태
    st.markdown("""
    <div class="emergency-card">
        <h2 style="color: white; margin: 0; font-size: 1.5rem;">⚠️ 긴급 출동 중</h2>
        <p style="color: #ffcdd2; margin: 5px 0; font-size: 1rem;">심정지 의심 환자 이송</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI 상황 요약
    st.markdown("""
    <div class="ai-summary">
        <h3 style="color: #00d4ff; margin-top: 0;">🤖 AI 상황 요약 (Context)</h3>
        <div style="color: white; line-height: 1.8;">
            <p><strong>환자 정보:</strong> 60대 남성 (추정 65세)</p>
            <p><strong>주 증상:</strong> 갑작스러운 가슴 통증 후 의식 소실</p>
            <p><strong>추정 상황:</strong> 심정지 의심 (심근경색 가능성 높음)</p>
            <p><strong>의식 상태:</strong> 무반응 (GCS 3점)</p>
            <p><strong>발견 장소:</strong> 서울시 중구 명동역 인근 (인파 밀집 지역)</p>
            <p><strong>신고자 진술 요약:</strong> "갑자기 쓰러졌어요! 숨을 안 쉬는 것 같아요!"</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 실시간 처치 가이드
    st.markdown("""
    <div class="treatment-guide">
        <h3 style="color: #ce93d8; margin-top: 0;">💊 실시간 처치 가이드</h3>
        <div style="color: white;">
            <p class="priority-high">🔴 우선순위 1: CPR 지속 (현재 5분 경과)</p>
            <p class="priority-high">🔴 우선순위 2: AED 준비 및 제세동 대기</p>
            <p class="priority-medium">🟡 우선순위 3: 정맥로 확보 (이송 중 시행)</p>
            <p class="priority-low">🟢 우선순위 4: 산소 투여 준비</p>
        </div>
        <div style="background: rgba(255, 255, 255, 0.1); padding: 10px; margin-top: 10px; border-radius: 5px;">
            <strong style="color: #ffeb3b;">⚡ AI 권고사항:</strong><br>
            <span style="color: #fff9c4;">심정지 의심 환자, 즉시 가장 가까운 권역외상센터 또는 심혈관센터로 이송 권장</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 6G 네트워크 상태
    st.markdown("### 📡 6G 네트워크 상태 (KPI)")
    
    # URLLC 상태
    urllc_active = True
    latency = np.random.uniform(15, 28)
    bandwidth = np.random.uniform(450, 500)
    
    net_col1, net_col2, net_col3 = st.columns(3)
    
    with net_col1:
        urllc_status = "✅ 활성화" if urllc_active else "❌ 비활성화"
        status_class = "network-status" if urllc_active else "network-status critical"
        st.markdown(f"""
        <div class="{status_class}">
            <div style="text-align: center;">
                <div class="metric-label">URLLC 전용 차선</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: {'#4caf50' if urllc_active else '#f44336'}; margin-top: 5px;">
                    {urllc_status}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with net_col2:
        latency_class = "network-status" if latency < 30 else "network-status warning"
        st.markdown(f"""
        <div class="{latency_class}">
            <div style="text-align: center;">
                <div class="metric-label">지연 시간 (Latency)</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: {'#4caf50' if latency < 30 else '#ff9800'}; margin-top: 5px;">
                    {latency:.1f}ms
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with net_col3:
        st.markdown(f"""
        <div class="network-status">
            <div style="text-align: center;">
                <div class="metric-label">대역폭</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #4caf50; margin-top: 5px;">
                    {bandwidth:.0f} Mbps
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # KOI (운영 성과 지표)
    st.markdown("### 📊 KOI (운영 성과 지표)")
    koi_col1, koi_col2, koi_col3 = st.columns(3)
    
    with koi_col1:
        st.markdown("""
        <div class="network-status">
            <div style="text-align: center;">
                <div class="metric-label">운영목표달성도</div>
                <div style="font-size: 2rem; font-weight: 700; color: #ff9800; margin-top: 5px;">
                    0.87
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with koi_col2:
        st.markdown("""
        <div class="network-status">
            <div style="text-align: center;">
                <div class="metric-label">비용효율성</div>
                <div style="font-size: 2rem; font-weight: 700; color: #ffa726; margin-top: 5px;">
                    0.90
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with koi_col3:
        st.markdown("""
        <div class="network-status">
            <div style="text-align: center;">
                <div class="metric-label">안정성지수</div>
                <div style="font-size: 2rem; font-weight: 700; color: #4caf50; margin-top: 5px;">
                    0.98
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Selective Active RIS 제어
    st.markdown("### 🔧 Selective Active RIS 제어")
    
    if 'ris_approved' not in st.session_state:
        st.session_state.ris_approved = False
    
    if not st.session_state.ris_approved:
        st.markdown("""
        <div style="background: rgba(255, 152, 0, 0.2); border: 2px solid #ff9800; border-radius: 10px; padding: 20px; margin: 15px 0;">
            <h4 style="color: #ffa726; margin-top: 0;">⚠️ Selective Active RIS 활성화 필요</h4>
            <p style="color: white; line-height: 1.8;">
                <strong>상황:</strong> 명동역 인근 불확실성 감지 (인파 밀집도 증가)<br>
                <strong>현재 모드:</strong> Passive RIS (기본 모드)<br>
                <strong>권장 조치:</strong> Active RIS로 전환하여 신호 품질 및 통신 안정성 향상
            </p>
            <div style="background: rgba(0, 0, 0, 0.3); padding: 10px; border-radius: 5px; margin-top: 10px;">
                <p style="color: #ffcc80; margin: 0; font-size: 0.95rem;">
                    <strong>⚡ Active RIS 효과:</strong><br>
                    • 신호 증폭률: +32dB → +45dB 향상<br>
                    • 링크 품질 개선 (Middle 통화실성 지표 상승)<br>
                    • 에이전트 AI의 비용 대비 효과 분석 완료
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_ris1, col_ris2 = st.columns(2)
        with col_ris1:
            if st.button("✅ Active RIS 활성화 승인", key="approve_ris", use_container_width=True):
                st.session_state.ris_approved = True
                st.rerun()
        with col_ris2:
            if st.button("❌ 현재 모드 유지", key="deny_ris", use_container_width=True):
                st.info("Passive RIS 모드를 유지합니다.")
    else:
        st.success("✅ Active RIS 모드가 활성화되었습니다!")
        st.markdown("""
        <div style="background: rgba(76, 175, 80, 0.2); border: 2px solid #4caf50; border-radius: 10px; padding: 15px; margin: 15px 0;">
            <p style="color: white; line-height: 1.8; margin: 0;">
                <strong style="color: #81c784;">📡 Active RIS 상태:</strong><br>
                • 신호 증폭률: +45dB (High Performance Mode)<br>
                • 링크 품질: 우수 (Middle 지표 98.5%)<br>
                • 패턴 기반 자동 전환: 활성화됨<br>
                • 예상 추가 비용: 최소 (고품질 라벨)
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Passive 모드로 복귀", key="reset_ris"):
            st.session_state.ris_approved = False
            st.rerun()
    
    # 네트워크 제어 로그
    st.markdown("### 📋 네트워크 제어 로그")
    
    if st.session_state.ris_approved:
        log_content = f"""
        [{current_time.strftime('%H:%M:%S')}] 🚨 긴급 출동 감지 → URLLC 모드 자동 활성화<br>
        [{(current_time - timedelta(seconds=15)).strftime('%H:%M:%S')}] 📍 명동역 인근 인파 밀집 감지 (밀도: 8.2명/m²)<br>
        [{(current_time - timedelta(seconds=30)).strftime('%H:%M:%S')}] ⚡ <strong style="color: #4caf50;">Selective Active RIS 모드 활성화 승인됨</strong><br>
        [{(current_time - timedelta(seconds=35)).strftime('%H:%M:%S')}] 🔄 Active RIS 반사 모드 가동 중 (신호 증폭률: +45dB)<br>
        [{(current_time - timedelta(seconds=45)).strftime('%H:%M:%S')}] 🌐 6G AI Agent: 최적 경로 재계산 완료<br>
        [{(current_time - timedelta(seconds=60)).strftime('%H:%M:%S')}] ✅ 병원 3곳과 데이터 동기화 완료<br>
        [{(current_time - timedelta(seconds=75)).strftime('%H:%M:%S')}] 🔐 양자 보안 채널 수립 완료
        """
    else:
        log_content = f"""
        [{current_time.strftime('%H:%M:%S')}] 🚨 긴급 출동 감지 → URLLC 모드 자동 활성화<br>
        [{(current_time - timedelta(seconds=15)).strftime('%H:%M:%S')}] 📍 명동역 인근 인파 밀집 감지 (밀도: 8.2명/m²)<br>
        [{(current_time - timedelta(seconds=30)).strftime('%H:%M:%S')}] 🔄 RIS 반사 모드 가동 중 (신호 증폭률: +32dB)<br>
        [{(current_time - timedelta(seconds=45)).strftime('%H:%M:%S')}] 🌐 6G AI Agent: 최적 경로 재계산 완료<br>
        [{(current_time - timedelta(seconds=60)).strftime('%H:%M:%S')}] ✅ 병원 3곳과 데이터 동기화 완료<br>
        [{(current_time - timedelta(seconds=75)).strftime('%H:%M:%S')}] 🔐 양자 보안 채널 수립 완료
        """
    
    st.markdown(f"""
    <div class="network-log">
        {log_content}
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("### 🏥 최적 병원 리스트")
    st.markdown('<p style="color: #90caf9; margin-bottom: 20px;">AI 에이전트가 계산한 최적 병원 목록입니다. 병원을 클릭하면 상세 정보를 확인할 수 있습니다.</p>', unsafe_allow_html=True)
    
    # 병원 데이터
    hospitals = [
        {
            "name": "서울대학교병원 권역외상센터",
            "distance": "2.3 km",
            "eta": "7분 30초",
            "available": True,
            "beds": "3개 가용",
            "specialists": "심장내과 전문의 2명 대기",
            "equipment": "심혈관조영술(CAG) 준비 완료",
            "score": 98
        },
        {
            "name": "서울아산병원 응급의료센터",
            "distance": "4.1 km",
            "eta": "11분 20초",
            "available": True,
            "beds": "5개 가용",
            "specialists": "순환기내과 전문의 3명 대기",
            "equipment": "중환자실 즉시 가용",
            "score": 95
        },
        {
            "name": "삼성서울병원 심장센터",
            "distance": "5.8 km",
            "eta": "14분 50초",
            "available": True,
            "beds": "2개 가용",
            "specialists": "심혈관외과 전문의 1명 대기",
            "equipment": "ECMO 장비 대기",
            "score": 92
        },
        {
            "name": "중앙대학교병원",
            "distance": "3.5 km",
            "eta": "9분 40초",
            "available": False,
            "beds": "포화 상태",
            "specialists": "대기 중",
            "equipment": "준비 중",
            "score": 75
        }
    ]
    
    # 병원 카드 렌더링
    for idx, hospital in enumerate(hospitals):
        if hospital["available"]:
            card_style = "hospital-card"
            availability_text = f"<span style='color: #4caf50; font-weight: 700;'>✅ 수용 가능</span>"
        else:
            card_style = "hospital-card" 
            availability_text = f"<span style='color: #f44336; font-weight: 700;'>❌ 수용 불가</span>"
        
        with st.container():
            st.markdown(f"""
            <div class="{card_style}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h3 style="color: #00d4ff; margin: 0;">{hospital['name']}</h3>
                    <div style="background: rgba(0, 212, 255, 0.2); padding: 5px 15px; border-radius: 20px;">
                        <span style="color: #00d4ff; font-weight: 700;">AI 점수: {hospital['score']}</span>
                    </div>
                </div>
                <div style="color: white; line-height: 1.6;">
                    <p><strong>📍 거리:</strong> {hospital['distance']} | <strong>⏱️ ETA:</strong> {hospital['eta']}</p>
                    <p><strong>🛏️ 병상:</strong> {hospital['beds']} | <strong>👨‍⚕️ 전문의:</strong> {hospital['specialists']}</p>
                    <p><strong>🔬 장비:</strong> {hospital['equipment']}</p>
                    <p><strong>수용 여부:</strong> {availability_text}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 병원 선택 버튼
            if st.button(f"🏥 {hospital['name']} 상세보기", key=f"hospital_{idx}", disabled=not hospital["available"]):
                st.session_state.selected_hospital = hospital

# 선택된 병원의 병원 관제 화면으로 전환
if st.session_state.selected_hospital:
    st.markdown("---")
    st.markdown(f"### 🔄 {st.session_state.selected_hospital['name']} 관제 화면으로 전환됩니다...")
    st.markdown("**아래 버튼을 클릭하여 병원 관제 대시보드를 확인하세요.**")
    
    if st.button("🏥 병원 관제 화면 보기", type="primary"):
        st.info("💡 별도 탭에서 `hospital_dashboard.py`를 실행하여 병원 관제 화면을 확인하세요.")
        st.code("streamlit run hospital_dashboard.py", language="bash")

# 자동 새로고침 (실시간 업데이트 시뮬레이션)
if st.checkbox("🔄 실시간 업데이트 활성화", value=False):
    time.sleep(2)
    st.rerun()
