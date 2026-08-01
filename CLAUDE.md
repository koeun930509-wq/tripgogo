# CLAUDE.md

이 파일은 이 저장소에서 코드 작업을 할 때 Claude Code(claude.ai/code)에게 제공되는 안내 문서입니다.

## 프로젝트 현황

- `PRD.md` — 제품 요구사항 문서
- `backend/` — 핵심 추천 로직 모듈 (Flask 앱으로 아직 감싸지 않은 상태, 콘솔에서 직접 실행 가능)
- 프론트엔드(React + Vite)는 아직 스캐폴딩되지 않았습니다.

### backend 실행 방법

```
cd backend
pip install -r requirements.txt
cp .env.example .env   # KAKAO_REST_API_KEY, OPENWEATHER_API_KEY, GEMINI_API_KEY 채워넣기
python pipeline.py "제주도" "2026-08-01"
```

`pipeline.py`의 `get_travel_recommendation(region, date)`가 카카오맵 geocoding → OpenWeatherMap 날씨 조회 → Gemini 추천 생성을 순서대로 호출하는 진입점입니다. OpenWeatherMap 무료 티어는 최대 5일 이내 날짜만 예보를 제공합니다.

아직 린트/테스트 도구는 구성돼 있지 않습니다. Flask 엔드포인트나 프론트엔드가 추가되면 이 섹션을 업데이트해야 합니다.

## 제품: 팀트립고고 (TripGoGo)

사용자가 지역과 여행 날짜를 선택하면, 날씨를 고려한 추천 결과 — 유명 관광지 + 숨겨진 현지 명소, 그리고 현지 맛집/음식 추천 — 을 보여주는 반응형 웹앱입니다. 전체 스펙은 `PRD.md`에 있습니다.

## 의도된 아키텍처 (PRD.md 기준)

- **프론트엔드**: React + Vite (아직 미구현)
- **백엔드**: Python 3.11 + Flask (`backend/` 핵심 로직은 구현됨, Flask 엔드포인트로 감싸는 작업은 아직)
- **AI 추천**: Gemini — 반드시 `google-genai` SDK를 사용해야 합니다. 구버전 `google-generativeai` 패키지는 **사용 금지**입니다.
- **외부 API**: 위경도 변환은 카카오맵 API(`backend/services/kakao_service.py`), 날씨 조회는 OpenWeatherMap(`backend/services/weather_service.py`), 명소·맛집 추천 생성은 Gemini(`backend/services/gemini_service.py`)로 확정.

핵심 흐름: 지역 + 날짜 입력 → 해당 지역·날짜의 날씨 조회 → 날씨와 지역 정보를 Gemini에 전달해 추천 생성(유명 명소 + 숨겨진 현지 명소 + 현지 음식) → React UI에 결과 렌더링.

프로젝트를 스캐폴딩할 때는 PRD의 스택 제약에 따라 프론트엔드(`React + Vite`)와 백엔드(`Flask`)를 분리하고, 날씨 조회·지도 API 호출·Gemini 호출은 백엔드가 담당하며, 프론트엔드는 입력 UI와 결과 렌더링만 담당하도록 합니다.
