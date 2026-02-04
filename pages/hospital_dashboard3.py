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
    page_title="🏥 FIELD-DREAM 병원 관제 대시보드",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링
st.markdown("""
<style>
    /* 전체 배경 및 폰트 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1a237e 0%, #0d1b2a 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 메인 타이틀 */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00e676 0%, #00bfa5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 0 30px rgba(0, 230, 118, 0.5);
    }
    
    /* 수신 환자 카드 */
    .patient-card {
        background: linear-gradient(135deg, rgba(255, 87, 34, 0.2) 0%, rgba(230, 74, 25, 0.2) 100%);
        border: 2px solid #ff5722;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(255, 87, 34, 0.4);
    }
    
    /* 바이탈 사인 카드 */
    .vital-signs {
        background: rgba(0, 150, 136, 0.15);
        border: 2px solid #009688;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .vital-item {
        background: rgba(0, 0, 0, 0.3);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #00e676;
    }
    
    .vital-critical {
        border-left-color: #ff5252;
        animation: blink 1.5s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* 보안 마크 */
    .security-badge {
        background: linear-gradient(135deg, #7c4dff 0%, #651fff 100%);
        border: 2px solid #b388ff;
        border-radius: 10px;
        padding: 10px 20px;
        display: inline-block;
        margin: 10px 5px;
        box-shadow: 0 4px 16px rgba(124, 77, 255, 0.4);
    }
    
    /* 영상 스트리밍 영역 */
    .video-stream {
        background: rgba(0, 0, 0, 0.5);
        border: 3px solid #00e676;
        border-radius: 15px;
        padding: 20px;
        min-height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }
    
    .video-stream::before {
        content: "📹 실시간 6G 영상 스트리밍";
        position: absolute;
        top: 10px;
        left: 10px;
        background: rgba(0, 230, 118, 0.9);
        color: white;
        padding: 5px 15px;
        border-radius: 5px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    .video-stream::after {
        content: "🔴 LIVE";
        position: absolute;
        top: 10px;
        right: 10px;
        background: #ff1744;
        color: white;
        padding: 5px 15px;
        border-radius: 5px;
        font-weight: 700;
        font-size: 0.9rem;
        animation: pulse 2s infinite;
    }
    
    /* ETA 카운터 */
    .eta-counter {
        background: linear-gradient(135deg, #ff6f00 0%, #e65100 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 111, 0, 0.5);
    }
    
    .eta-time {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        color: white;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
    }
    
    /* 수용 결정 버튼 */
    .accept-button {
        background: linear-gradient(135deg, #00e676 0%, #00c853 100%);
        color: white;
        font-weight: 900;
        border: none;
        border-radius: 15px;
        padding: 20px 40px;
        font-size: 1.3rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 230, 118, 0.5);
        width: 100%;
        margin: 10px 0;
    }
    
    .accept-button:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 48px rgba(0, 230, 118, 0.8);
    }
    
    .reject-button {
        background: linear-gradient(135deg, #ff1744 0%, #d50000 100%);
        color: white;
        font-weight: 900;
        border: none;
        border-radius: 15px;
        padding: 20px 40px;
        font-size: 1.3rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(255, 23, 68, 0.5);
        width: 100%;
        margin: 10px 0;
    }
    
    .reject-button:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 48px rgba(255, 23, 68, 0.8);
    }
    
    /* 타 병원 요청 카드 */
    .transfer-card {
        background: rgba(255, 152, 0, 0.15);
        border: 2px solid #ff9800;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .nearby-hospital {
        background: rgba(0, 0, 0, 0.3);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .nearby-hospital:hover {
        border-color: #ff9800;
        background: rgba(255, 152, 0, 0.2);
        transform: translateX(5px);
    }
    
    /* 메트릭 */
    .metric-label {
        font-size: 0.9rem;
        color: #80deea;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #00e676;
        margin: 5px 0;
    }
    
    /* 트리아지 배지 */
    .triage-critical {
        background: #ff1744;
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-weight: 900;
        font-size: 1.1rem;
        display: inline-block;
        box-shadow: 0 4px 16px rgba(255, 23, 68, 0.6);
    }
    
    .triage-urgent {
        background: #ff9800;
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-weight: 900;
        font-size: 1.1rem;
        display: inline-block;
    }
    
    .triage-normal {
        background: #4caf50;
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'patient_accepted' not in st.session_state:
    st.session_state.patient_accepted = None
if 'eta_seconds' not in st.session_state:
    st.session_state.eta_seconds = 7 * 60 + 30  # 7분 30초
if 'transfer_requested' not in st.session_state:
    st.session_state.transfer_requested = False

# 헤더
st.markdown('<h1 class="main-title">🏥 FIELD-DREAM 병원 관제 대시보드</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #80deea; font-size: 1.2rem; margin-bottom: 30px;">서울대학교병원 권역외상센터</p>', unsafe_allow_html=True)

# 현재 시간
current_time = datetime.now()
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="metric-label">현재 시각</div>
        <div class="metric-value">{current_time.strftime('%H:%M:%S')}</div>
    </div>
    """, unsafe_allow_html=True)

with col_info2:
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="metric-label">가용 병상</div>
        <div class="metric-value" style="color: #00e676;">3개</div>
    </div>
    """, unsafe_allow_html=True)

with col_info3:
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="metric-label">대기 전문의</div>
        <div class="metric-value" style="color: #00e676;">2명</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 메인 레이아웃
col_left, col_right = st.columns([1.2, 1])

with col_left:
    # 수신 환자 정보
    st.markdown("""
    <div class="patient-card">
        <h2 style="color: #ff7043; margin-top: 0;">🚑 수신 환자 정보</h2>
        <div style="color: white; line-height: 1.8;">
            <p><strong>사건 번호:</strong> EMG-2025-0203-7842</p>
            <p><strong>발생 시각:</strong> 14:23:15</p>
            <p><strong>발생 장소:</strong> 서울시 중구 명동역 인근</p>
            <p><strong>전송 구급대:</strong> 서울중부소방서 119구급대</p>
            <p><strong>구급대원:</strong> 김응급, 박구조</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # AI 중증도 분류
    st.markdown("### 🤖 AI 중증도 분류 (Triage)")
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <div class="triage-critical">⚠️ 최우선 (Critical) - Level 1</div>
    </div>
    <div style="background: rgba(255, 23, 68, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #ff1744; margin-top: 15px;">
        <p style="color: white; line-height: 1.8; margin: 0;">
            <strong style="color: #ff7043;">AI 분석 결과:</strong><br>
            심정지 또는 심근경색 가능성 매우 높음 (신뢰도 94.7%)<br>
            즉각적인 중환자실 및 심혈관조영술(CAG) 준비 필요<br>
            예상 필요 시술: PCI (경피적 관상동맥 중재술)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 바이탈 사인
    st.markdown("### 💓 실시간 바이탈 사인")
    st.markdown("""
    <div class="vital-signs">
        <div class="vital-item vital-critical">
            <strong style="color: #ff5252;">❤️ 심박수:</strong> 
            <span style="color: white; font-size: 1.3rem; font-weight: 700; margin-left: 10px;">38 BPM</span>
            <span style="color: #ff7043; margin-left: 15px; font-weight: 700;">⚠️ 심각한 서맥</span>
        </div>
        <div class="vital-item vital-critical">
            <strong style="color: #ff5252;">🩸 혈압:</strong> 
            <span style="color: white; font-size: 1.3rem; font-weight: 700; margin-left: 10px;">80/45 mmHg</span>
            <span style="color: #ff7043; margin-left: 15px; font-weight: 700;">⚠️ 저혈압</span>
        </div>
        <div class="vital-item">
            <strong style="color: #00e676;">🫁 호흡수:</strong> 
            <span style="color: white; font-size: 1.3rem; font-weight: 700; margin-left: 10px;">8 /min</span>
            <span style="color: #ffb74d; margin-left: 15px; font-weight: 700;">⚠️ 서맥성 호흡</span>
        </div>
        <div class="vital-item">
            <strong style="color: #00e676;">🌡️ 체온:</strong> 
            <span style="color: white; font-size: 1.3rem; font-weight: 700; margin-left: 10px;">35.8°C</span>
            <span style="color: #81c784; margin-left: 15px;">정상 범위</span>
        </div>
        <div class="vital-item vital-critical">
            <strong style="color: #ff5252;">💨 산소포화도:</strong> 
            <span style="color: white; font-size: 1.3rem; font-weight: 700; margin-left: 10px;">82%</span>
            <span style="color: #ff7043; margin-left: 15px; font-weight: 700;">⚠️ 저산소증</span>
        </div>
        <div class="vital-item">
            <strong style="color: #00e676;">🧠 의식 수준 (GCS):</strong> 
            <span style="color: white; font-size: 1.3rem; font-weight: 700; margin-left: 10px;">3점</span>
            <span style="color: #ff7043; margin-left: 15px; font-weight: 700;">⚠️ 심각한 의식 저하</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 실시간 영상 스트리밍
    st.markdown("### 📹 실시간 영상 스트리밍")
    st.markdown("""
    <div class="video-stream">
        <div style="text-align: center; color: white;">
            <div style="font-size: 4rem; margin-bottom: 10px;">📹</div>
            <p style="font-size: 1.2rem; font-weight: 700;">6G 고대역폭 영상 전송 중</p>
            <p style="color: #80deea;">해상도: 4K (3840×2160) | 프레임률: 60fps</p>
            <p style="color: #4caf50; font-weight: 700;">📶 연결 상태: 우수 (대역폭 487 Mbps)</p>
            <div style="margin-top: 20px; background: rgba(0, 0, 0, 0.5); padding: 15px; border-radius: 10px; display: inline-block;">
                <p style="margin: 0; color: #ffb74d;">현재 환자 상태 영상 실시간 전송 중</p>
                <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #90caf9;">CPR 진행 상황 확인 가능</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    # ETA 카운터
    st.markdown("### ⏱️ 도착 예정 시간 (ETA)")
    
    minutes = st.session_state.eta_seconds // 60
    seconds = st.session_state.eta_seconds % 60
    
    st.markdown(f"""
    <div class="eta-counter">
        <div class="eta-time">{minutes:02d}:{seconds:02d}</div>
        <p style="color: white; font-size: 1.1rem; margin: 10px 0 0 0;">실시간 교통 상황 반영</p>
        <p style="color: #ffcc80; font-size: 0.9rem; margin: 5px 0 0 0;">6G AI Agent가 최적 경로로 안내 중</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 데이터 보안 상태
    st.markdown("### 🔐 데이터 신뢰성 및 보안")
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <div class="security-badge">
            <span style="color: white; font-weight: 700;">🔒 양자 보안 (Quantum Security) 적용</span>
        </div>
        <div class="security-badge">
            <span style="color: white; font-weight: 700;">✅ 데이터 무결성 확인 완료</span>
        </div>
        <div class="security-badge">
            <span style="color: white; font-weight: 700;">🛡️ End-to-End 암호화</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(124, 77, 255, 0.15); padding: 15px; border-radius: 10px; border: 2px solid #7c4dff; margin-top: 15px;">
        <p style="color: white; line-height: 1.8; margin: 0;">
            <strong style="color: #b388ff;">🔐 보안 상태:</strong><br>
            ✓ 양자 키 분배(QKD) 프로토콜 활성화<br>
            ✓ 의료 데이터 HIPAA 준수<br>
            ✓ 블록체인 기반 전송 로그 기록<br>
            ✓ 무단 접근 시도: 0건
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 추가 정보
    st.markdown("### 📊 추가 의료 정보")
    st.markdown("""
    <div style="background: rgba(0, 188, 212, 0.15); padding: 15px; border-radius: 10px; border: 2px solid #00bcd4;">
        <p style="color: white; line-height: 1.8;">
            <strong style="color: #4dd0e1;">환자 과거력 (AI 분석):</strong><br>
            • 고혈압 병력 (5년)<br>
            • 당뇨병 (3년)<br>
            • 흡연력: 30갑년<br>
            • 최근 흉통 호소 이력 있음<br>
            • 알러지: 페니실린 계열
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(255, 193, 7, 0.15); padding: 15px; border-radius: 10px; border: 2px solid #ffc107; margin-top: 15px;">
        <p style="color: white; line-height: 1.8;">
            <strong style="color: #ffd54f;">⚡ 구급대원 현장 조치:</strong><br>
            • CPR 진행 중 (8분 경과)<br>
            • 기도 확보 완료<br>
            • 산소 투여 중 (15L/min)<br>
            • 정맥로 확보 시도 중<br>
            • AED 제세동 1회 시행
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 수용 결정 인터페이스
st.markdown("## 🏥 수용 결정")

if st.session_state.patient_accepted is None:
    col_accept, col_reject = st.columns(2)
    
    with col_accept:
        if st.button("✅ 환자 수용 승인", key="accept", use_container_width=True):
            st.session_state.patient_accepted = True
            st.rerun()
    
    with col_reject:
        if st.button("❌ 수용 불가", key="reject", use_container_width=True):
            st.session_state.patient_accepted = False
            st.rerun()

elif st.session_state.patient_accepted == True:
    st.success("✅ 환자 수용이 승인되었습니다!")
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(0, 230, 118, 0.2) 0%, rgba(0, 200, 83, 0.2) 100%); 
                padding: 20px; border-radius: 15px; border: 2px solid #00e676; margin: 20px 0;">
        <h3 style="color: #00e676; margin-top: 0;">📋 수용 준비 체크리스트</h3>
        <div style="color: white; line-height: 2;">
            <p>✅ 중환자실 병상 확보 완료</p>
            <p>✅ 심혈관조영술(CAG) 장비 준비 완료</p>
            <p>✅ 심장내과 전문의 2명 대기</p>
            <p>✅ 응급실 소생술팀 소집 완료</p>
            <p>✅ 혈액은행 통보 완료 (O형 RBC 4unit 준비)</p>
            <p>🔄 심혈관중재시술팀 호출 중...</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 결정 취소", key="cancel"):
        st.session_state.patient_accepted = None
        st.rerun()

elif st.session_state.patient_accepted == False:
    st.error("❌ 환자 수용이 거부되었습니다.")
    
    # 타 병원 전원 요청
    st.markdown("### 🏥 근처 병원 전원 요청")
    
    if not st.session_state.transfer_requested:
        st.markdown("""
        <div class="transfer-card">
            <h3 style="color: #ff9800; margin-top: 0;">📍 근처 가용 병원</h3>
            <p style="color: #ffcc80;">수용이 불가능한 경우 근처 병원에 전원을 요청할 수 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
        nearby_hospitals = [
            {"name": "서울아산병원 응급의료센터", "distance": "4.1 km", "beds": "5개 가용", "score": 95},
            {"name": "삼성서울병원 심장센터", "distance": "5.8 km", "beds": "2개 가용", "score": 92},
            {"name": "세브란스병원 심혈관센터", "distance": "6.2 km", "beds": "4개 가용", "score": 90},
        ]
        
        selected_hospitals = []
        
        for idx, hospital in enumerate(nearby_hospitals):
            col_h1, col_h2 = st.columns([3, 1])
            
            with col_h1:
                st.markdown(f"""
                <div class="nearby-hospital">
                    <h4 style="color: #ff9800; margin: 0;">{hospital['name']}</h4>
                    <p style="color: white; margin: 5px 0;">
                        📍 {hospital['distance']} | 🛏️ {hospital['beds']} | AI 점수: {hospital['score']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_h2:
                if st.checkbox("선택", key=f"nearby_{idx}"):
                    selected_hospitals.append(hospital['name'])
        
        if selected_hospitals:
            st.markdown(f"**선택된 병원:** {', '.join(selected_hospitals)}")
            
            if st.button("📤 선택한 병원에 전원 요청 전송", type="primary"):
                st.session_state.transfer_requested = True
                st.rerun()
    else:
        st.success("✅ 전원 요청이 전송되었습니다!")
        st.markdown("""
        <div style="background: rgba(0, 230, 118, 0.15); padding: 15px; border-radius: 10px; border: 2px solid #00e676;">
            <p style="color: white; line-height: 1.8;">
                <strong style="color: #00e676;">전원 요청 상태:</strong><br>
                • 서울아산병원: 검토 중...<br>
                • 삼성서울병원: 검토 중...<br>
                • AI Agent가 실시간으로 응답을 모니터링하고 있습니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 다시 결정하기", key="reset"):
            st.session_state.patient_accepted = None
            st.session_state.transfer_requested = False
            st.rerun()

# 자동 ETA 업데이트
if st.checkbox("🔄 실시간 업데이트 활성화", value=False):
    if st.session_state.eta_seconds > 0:
        st.session_state.eta_seconds -= 1
    time.sleep(1)
    st.rerun()
