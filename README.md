# Emergency Management System

긴급 관리 시스템 - Streamlit 기반 다중 대시보드 애플리케이션

## 📋 프로젝트 개요

Emergency Management System은 현장 응급 관리, 병원 모니터링, 구급차 관리 등 다양한 업무를 통합으로 관리할 수 있는 대시보드 시스템입니다.

## 🎯 주요 기능

- **Front Office**: 현장 응급 관리 대시보드
  - 신고음성, 웨어러블 기록, 현장 처치 기록, 영상 스트리밍 시뮬레이션
  - 응급 상황 다양한 케이스 생성

- **Mid Office (병원 대시보드)**: 병원 및 구급 현황 모니터링
  - 환자 수용 결정 시스템
  - AI 중증도 분류 (Triage)
  - 실시간 바이탈 사인 모니터링

- **Mid Office (구급대원 대시보드)**: 구급대원용 응급 처치 가이드
  - AI 상황 요약 및 추천 병원
  - 실시간 처치 가이드
  - 환자별 맞춤형 프로토콜

- **Back Office**: 시스템 관리 및 설정
  - 6G RIS (Reconfigurable Intelligent Surfaces) 시각화
  - 신호 품질 개선 효과 분석
  - 시스템 모니터링

## 🚀 시작하기

### 필수 요구사항
- Python 3.8 이상
- pip

### 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/bbongappang/pages.git
cd pages
```

2. 필수 패키지 설치
```bash
pip install -r requirements.txt
```

3. Streamlit 앱 실행
```bash
streamlit run main.py
```

## 📁 프로젝트 구조

```
.
├── main.py                           # 메인 진입점 (네비게이션)
├── pages/
│   ├── front_dashboard.py            # 현장 응급 관리 대시보드
│   ├── hospital_dashboard3.py        # 병원 관제 대시보드
│   ├── paramedic_dashboard3.py       # 구급대원 대시보드
│   └── back_office_dashboard.py      # 백오피스 시스템 관리
├── requirements.txt                  # 필수 Python 패키지
└── README.md                         # 프로젝트 설명
```

## 🔧 기술 스택

- **Streamlit**: 웹 애플리케이션 프레임워크
- **Pandas**: 데이터 분석 및 조작
- **NumPy**: 수치 계산
- **Plotly**: 대화형 데이터 시각화

## 📝 라이센스

MIT License

## 👤 작성자

@bbongappang

## 🤝 기여

프로젝트 개선을 위한 이슈 제출 및 풀 리퀘스트를 환영합니다.
