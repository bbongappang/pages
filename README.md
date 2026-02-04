# Emergency Management System

긴급 관리 시스템 - Streamlit 기반 다중 대시보드 애플리케이션

## 📋 프로젝트 개요

Emergency Management System은 현장 응급 관리, 병원 모니터링, 구급차 관리 등 다양한 업무를 통합으로 관리할 수 있는 대시보드 시스템입니다.

## 🎯 주요 기능

- **Front Office**: 현장 응급 관리 대시보드
- **Mid Office**: 병원 및 구급차 현황 모니터링
- **Back Office**: 시스템 관리 및 설정

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
streamlit run pages/main.py
```

## 📁 프로젝트 구조

```
.
├── app.py                     # 메인 진입점 (네비게이션)
├── pages/
│   ├── front_dashboard.py     # 현장 응급 관리 대시보드
│   ├── hospital_dashboard3.py # 병원 관제 대시보드
│   ├── paramedic_dashboard3.py # 구급차 관리 대시보드
│   └── back_office_dashboard.py # 백오피스 시스템 관리
├── requirements.txt           # 필수 Python 패키지
├── .streamlit/
│   └── config.toml           # Streamlit 설정
└── README.md                  # 프로젝트 설명
```

## 🔧 기술 스택

- **Streamlit**: 웹 애플리케이션 프레임워크
- **Pandas**: 데이터 분석 및 조작
- **NumPy**: 수치 계산

## 📝 라이센스

MIT License

## 👤 작성자

@bbongappang

## 🤝 기여

프로젝트 개선을 위한 이슈 제출 및 풀 리퀘스트를 환영합니다.
