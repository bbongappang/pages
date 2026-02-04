import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import streamlit as st

# 각 대시보드 파일 상단에 추가
if st.sidebar.button("🏠 메인 화면으로"):
    st.switch_page("main.py")

# 페이지 설정
st.set_page_config(
    page_title="🎯 FIELD-DREAM Front - 계층형 메모리",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링
st.markdown("""
<style>
    /* 전체 배경 */
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;700&family=Noto+Sans+KR:wght@300;400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 메인 타이틀 */
    .main-title {
        font-family: 'Fira Code', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #a78bfa;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* 데이터 흐름 카드 */
    .data-flow-card {
        background: rgba(102, 126, 234, 0.1);
        border: 2px solid #667eea;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    /* JSON 뷰어 스타일 */
    .json-viewer {
        background: rgba(0, 0, 0, 0.4);
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 15px;
        font-family: 'Fira Code', monospace;
        font-size: 0.85rem;
        color: #10b981;
        overflow-x: auto;
        margin: 10px 0;
    }
    
    .json-hot {
        border-left-color: #ef4444;
        color: #fca5a5;
    }
    
    .json-warm {
        border-left-color: #f59e0b;
        color: #fcd34d;
    }
    
    .json-cold {
        border-left-color: #3b82f6;
        color: #93c5fd;
    }
    
    /* 메모리 계층 표시 */
    .memory-layer {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.2) 100%);
        border: 2px solid #3b82f6;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .memory-layer:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
    }
    
    .memory-hot {
        border-color: #ef4444;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%);
    }
    
    .memory-warm {
        border-color: #f59e0b;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.2) 100%);
    }
    
    .memory-cold {
        border-color: #3b82f6;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.2) 100%);
    }
    
    /* 처리 단계 파이프라인 */
    .pipeline-stage {
        background: rgba(168, 85, 247, 0.15);
        border: 2px solid #a855f7;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        position: relative;
    }
    
    .pipeline-stage::before {
        content: "→";
        position: absolute;
        right: -20px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 2rem;
        color: #a855f7;
    }
    
    .pipeline-stage:last-child::before {
        content: "";
    }
    
    /* 스트림 라인 */
    .stream-line {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 8px;
        padding: 8px 12px;
        margin: 5px 0;
        font-family: 'Fira Code', monospace;
        font-size: 0.8rem;
        border-left: 3px solid #8b5cf6;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* 실시간 모니터 */
    .realtime-monitor {
        background: rgba(0, 0, 0, 0.5);
        border: 2px solid #10b981;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Fira Code', monospace;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .log-entry {
        color: #10b981;
        margin: 5px 0;
        padding: 5px;
        border-bottom: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .log-entry.error {
        color: #ef4444;
    }
    
    .log-entry.warning {
        color: #f59e0b;
    }
    
    .log-entry.info {
        color: #3b82f6;
    }
    
    /* 메트릭 */
    .metric-box {
        background: rgba(139, 92, 246, 0.15);
        border: 2px solid #8b5cf6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    
    .metric-value {
        font-family: 'Fira Code', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #a78bfa;
    }
    
    .metric-label {
        color: #c4b5fd;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    
    /* 태그 */
    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        margin: 2px;
    }
    
    .tag-hot {
        background: #ef4444;
        color: white;
    }
    
    .tag-warm {
        background: #f59e0b;
        color: white;
    }
    
    .tag-cold {
        background: #3b82f6;
        color: white;
    }
    
    .tag-processing {
        background: #8b5cf6;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'data_stream' not in st.session_state:
    st.session_state.data_stream = []
if 'processing_logs' not in st.session_state:
    st.session_state.processing_logs = []

# 헤더
st.markdown('<h1 class="main-title">🎯 FIELD-DREAM Front</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">계층형 메모리 & 실시간 데이터 처리 모니터링</p>', unsafe_allow_html=True)

# 현재 시간
current_time = datetime.now()

# 상단 메트릭
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">총 처리 데이터</div>
        <div class="metric-value">1,247</div>
        <div style="color: #10b981; font-size: 0.8rem;">▲ +89 (5분)</div>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">실시간 스트림</div>
        <div class="metric-value">23/s</div>
        <div style="color: #f59e0b; font-size: 0.8rem;">평균 처리 속도</div>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">메모리 사용률</div>
        <div class="metric-value">67%</div>
        <div style="color: #3b82f6; font-size: 0.8rem;">Hot: 12% | Warm: 28%</div>
    </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">처리 지연</div>
        <div class="metric-value">24ms</div>
        <div style="color: #10b981; font-size: 0.8rem;">✓ 정상 범위</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 메인 레이아웃
col_left, col_right = st.columns([1.3, 1])

with col_left:
    # 실시간 데이터 입력 스트림
    st.markdown("### 📥 실시간 데이터 입력 스트림")
    
    # 샘플 데이터 생성
    sample_emergency_data = {
        "source": "emergency_call",
        "type": "triage_text",
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "payload": {
            "text": "42세 여성, 교통사고 부상, 의식 명료"
        }
    }
    
    sample_vital_data = {
        "source": "ambulance_sensor",
        "type": "vital_signs",
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "payload": {
            "heart_rate": 92,
            "bp_systolic": 125,
            "bp_diastolic": 78,
            "spo2": 97,
            "temp": 36.8
        }
    }
    
    sample_location_data = {
        "source": "gps_tracker",
        "type": "location",
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "payload": {
            "lat": 37.5665,
            "lng": 126.9780,
            "speed": 45.2,
            "heading": "SE"
        }
    }
    
    tab1, tab2, tab3 = st.tabs(["🔴 Hot (긴급 호출)", "🟡 Warm (바이탈)", "🔵 Cold (위치)"])
    
    with tab1:
        st.markdown('<div class="tag tag-hot">HOT MEMORY</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="json-viewer json-hot">
{json.dumps(sample_emergency_data, indent=2, ensure_ascii=False)}
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="tag tag-warm">WARM MEMORY</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="json-viewer json-warm">
{json.dumps(sample_vital_data, indent=2, ensure_ascii=False)}
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="tag tag-cold">COLD MEMORY</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="json-viewer json-cold">
{json.dumps(sample_location_data, indent=2, ensure_ascii=False)}
        </div>
        """, unsafe_allow_html=True)
    
    # 데이터 처리 파이프라인
    st.markdown("### 🔄 데이터 처리 파이프라인 (3단계)")
    
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin: 20px 0;">
        <div class="pipeline-stage" style="flex: 1;">
            <h4 style="color: #a855f7; margin: 0;">Stage 1: 수집</h4>
            <p style="color: #c4b5fd; font-size: 0.9rem; margin: 5px 0;">원시 데이터 수신</p>
            <div class="tag tag-processing">RUNNING</div>
        </div>
        <div class="pipeline-stage" style="flex: 1;">
            <h4 style="color: #a855f7; margin: 0;">Stage 2: 분류</h4>
            <p style="color: #c4b5fd; font-size: 0.9rem; margin: 5px 0;">Hot/Warm/Cold 분류</p>
            <div class="tag tag-processing">RUNNING</div>
        </div>
        <div class="pipeline-stage" style="flex: 1;">
            <h4 style="color: #a855f7; margin: 0;">Stage 3: 전달</h4>
            <p style="color: #c4b5fd; font-size: 0.9rem; margin: 5px 0;">Mid 계층으로 전송</p>
            <div class="tag tag-processing">RUNNING</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 처리 상세 로그
    st.markdown("#### 📋 처리 상세 로그")
    
    processing_steps = [
        {
            "time": current_time.strftime("%H:%M:%S.%f")[:-3],
            "stage": "Stage 1",
            "action": "수신: emergency_call 데이터",
            "status": "✓"
        },
        {
            "time": (current_time - timedelta(milliseconds=150)).strftime("%H:%M:%S.%f")[:-3],
            "stage": "Stage 2",
            "action": "분류: HOT 메모리로 할당 (긴급도: 높음)",
            "status": "✓"
        },
        {
            "time": (current_time - timedelta(milliseconds=300)).strftime("%H:%M:%S.%f")[:-3],
            "stage": "Stage 3",
            "action": "전송: 구급대원/병원 대시보드로 전달",
            "status": "✓"
        },
        {
            "time": (current_time - timedelta(milliseconds=450)).strftime("%H:%M:%S.%f")[:-3],
            "stage": "Stage 1",
            "action": "수신: vital_signs 데이터",
            "status": "✓"
        },
        {
            "time": (current_time - timedelta(milliseconds=600)).strftime("%H:%M:%S.%f")[:-3],
            "stage": "Stage 2",
            "action": "분류: WARM 메모리로 할당 (주기적 업데이트)",
            "status": "✓"
        }
    ]
    
    log_html = ""
    for step in processing_steps:
        log_html += f"""
        <div class="stream-line">
            <span style="color: #6366f1;">[{step['time']}]</span>
            <span style="color: #a855f7; font-weight: 700;">{step['stage']}</span>
            <span style="color: #e0e7ff;"> → {step['action']}</span>
            <span style="color: #10b981;"> {step['status']}</span>
        </div>
        """
    
    st.markdown(f'<div style="max-height: 250px; overflow-y: auto;">{log_html}</div>', unsafe_allow_html=True)

with col_right:
    # 계층형 메모리 현황
    st.markdown("### 🗄️ 계층형 메모리 (Hot-Warm-Cold)")
    
    st.markdown("""
    <div class="memory-layer memory-hot">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="color: #ef4444; margin: 0;">🔴 Hot Memory (긴급 5분)</h4>
                <p style="color: #fca5a5; font-size: 0.85rem; margin: 5px 0;">초고속 접근 | 실시간 처리</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.8rem; font-weight: 700; color: #fca5a5;">148 MB</div>
                <div style="font-size: 0.8rem; color: #fecaca;">12% 사용 중</div>
            </div>
        </div>
        <div style="margin-top: 10px; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px;">
            <div style="color: #fecaca; font-size: 0.85rem;">
                • 긴급 호출 데이터: 23건<br>
                • 심정지 의심 환자: 2건<br>
                • AI 상황 분석 결과: 실시간 업데이트
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="memory-layer memory-warm">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="color: #f59e0b; margin: 0;">🟡 Warm Memory (20분)</h4>
                <p style="color: #fcd34d; font-size: 0.85rem; margin: 5px 0;">빠른 접근 | 주기적 업데이트</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.8rem; font-weight: 700; color: #fbbf24;">342 MB</div>
                <div style="font-size: 0.8rem; color: #fde68a;">28% 사용 중</div>
            </div>
        </div>
        <div style="margin-top: 10px; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px;">
            <div style="color: #fde68a; font-size: 0.85rem;">
                • 바이탈 사인 데이터: 15분간 기록<br>
                • 이송 중 환자 모니터링: 8건<br>
                • 병원 매칭 히스토리
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="memory-layer memory-cold">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="color: #3b82f6; margin: 0;">🔵 Cold Memory (아카이브)</h4>
                <p style="color: #93c5fd; font-size: 0.85rem; margin: 5px 0;">장기 보관 | 분석용 데이터</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.8rem; font-weight: 700; color: #60a5fa;">1.2 GB</div>
                <div style="font-size: 0.8rem; color: #bfdbfe;">27% 사용 중</div>
            </div>
        </div>
        <div style="margin-top: 10px; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px;">
            <div style="color: #bfdbfe; font-size: 0.85rem;">
                • GPS 위치 로그: 전체 이송 경로<br>
                • 네트워크 성능 이력<br>
                • 과거 출동 데이터 (30일)
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # API / 텔레메트리
    st.markdown("### 📡 API 설정 / 텔레메트리")
    
    st.markdown("""
    <div class="data-flow-card">
        <h4 style="color: #667eea; margin-top: 0;">설정된 API: 3개</h4>
        <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; margin: 10px 0;">
            <div style="color: #c7d2fe; font-family: 'Fira Code', monospace; font-size: 0.85rem;">
                <strong style="color: #818cf8;">POST</strong> /api/v1/network/slice<br>
                <span style="color: #a5b4fc;">→ 6G 네트워크 슬라이스 요청</span><br><br>
                
                <strong style="color: #fbbf24;">PUT</strong> /api/v1/ris/mode<br>
                <span style="color: #fde68a;">→ RIS Active/Passive 모드 전환</span><br><br>
                
                <strong style="color: #f472b6;">PATCH</strong> /api/v1/ai-ran/config<br>
                <span style="color: #fbcfe8;">→ AI-RAN 설정 업데이트</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 실시간 텔레메트리
    st.markdown("""
    <div class="data-flow-card">
        <h4 style="color: #667eea; margin-top: 0;">📊 실시간 텔레메트리</h4>
        <div style="color: #c7d2fe; line-height: 1.8;">
            • 평균 응답 시간: <strong style="color: #10b981;">18ms</strong><br>
            • API 호출 성공률: <strong style="color: #10b981;">99.8%</strong><br>
            • 동시 연결: <strong style="color: #f59e0b;">47개</strong><br>
            • 대기 큐: <strong style="color: #3b82f6;">2건</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 하단: 실시간 이벤트 모니터
st.markdown("### 📺 실시간 이벤트 모니터")

col_monitor1, col_monitor2 = st.columns(2)

with col_monitor1:
    st.markdown("#### 🟢 성공 로그")
    success_logs = [
        f"[{current_time.strftime('%H:%M:%S')}] ✓ 데이터 수신: emergency_call_7842",
        f"[{(current_time - timedelta(seconds=5)).strftime('%H:%M:%S')}] ✓ Hot 메모리 할당 완료",
        f"[{(current_time - timedelta(seconds=10)).strftime('%H:%M:%S')}] ✓ AI 트리아지 분석 완료 (Level 1)",
        f"[{(current_time - timedelta(seconds=15)).strftime('%H:%M:%S')}] ✓ 병원 3곳 데이터 전송 완료",
        f"[{(current_time - timedelta(seconds=20)).strftime('%H:%M:%S')}] ✓ RIS 모드 전환 요청 처리",
    ]
    
    log_html = ""
    for log in success_logs:
        log_html += f'<div class="log-entry">{log}</div>'
    
    st.markdown(f'<div class="realtime-monitor">{log_html}</div>', unsafe_allow_html=True)

with col_monitor2:
    st.markdown("#### 🟡 경고 / 정보")
    warning_logs = [
        f"[{current_time.strftime('%H:%M:%S')}] ⚠️ Warm 메모리 사용률 28% (정상)",
        f"[{(current_time - timedelta(seconds=8)).strftime('%H:%M:%S')}] ℹ️ Cold 데이터 아카이브 중...",
        f"[{(current_time - timedelta(seconds=12)).strftime('%H:%M:%S')}] ⚠️ API 지연 감지: 45ms (임계값: 50ms)",
        f"[{(current_time - timedelta(seconds=18)).strftime('%H:%M:%S')}] ℹ️ 네트워크 슬라이스 재할당 완료",
        f"[{(current_time - timedelta(seconds=25)).strftime('%H:%M:%S')}] ⚠️ 동시 연결 47개 (최대: 100)",
    ]
    
    log_html = ""
    for idx, log in enumerate(warning_logs):
        log_class = "warning" if "⚠️" in log else "info"
        log_html += f'<div class="log-entry {log_class}">{log}</div>'
    
    st.markdown(f'<div class="realtime-monitor">{log_html}</div>', unsafe_allow_html=True)

# 자동 새로고침
if st.checkbox("🔄 실시간 모니터링 활성화", value=False):
    time.sleep(1)
    st.rerun()
