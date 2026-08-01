from datetime import date, datetime, timedelta

import requests

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
MAX_FORECAST_DAYS = 16

# https://open-meteo.com/en/docs 의 WMO Weather interpretation codes
WEATHER_CODE_DESCRIPTIONS = {
    0: "맑음",
    1: "대체로 맑음",
    2: "구름 조금",
    3: "흐림",
    45: "안개",
    48: "짙은 안개",
    51: "약한 이슬비",
    53: "이슬비",
    55: "강한 이슬비",
    56: "약한 착빙성 이슬비",
    57: "강한 착빙성 이슬비",
    61: "약한 비",
    63: "비",
    65: "강한 비",
    66: "약한 착빙성 비",
    67: "강한 착빙성 비",
    71: "약한 눈",
    73: "눈",
    75: "강한 눈",
    77: "싸락눈",
    80: "약한 소나기",
    81: "소나기",
    82: "강한 소나기",
    85: "약한 소나기눈",
    86: "강한 소나기눈",
    95: "뇌우",
    96: "약한 우박을 동반한 뇌우",
    99: "강한 우박을 동반한 뇌우",
}


def _describe_weather_code(code: int) -> str:
    return WEATHER_CODE_DESCRIPTIONS.get(code, "알 수 없음")


def _travel_index(temp_max: float, pop: int, windspeed: float, humidity: int) -> str:
    """기온·강수확률·풍속·습도를 종합한 간단한 여행 적합도 지수를 반환한다."""
    if pop >= 70 or windspeed >= 40 or temp_max >= 35:
        return "나쁨"
    if pop >= 40 or windspeed >= 25 or humidity >= 80 or temp_max >= 31:
        return "보통"
    return "좋음"


def _validate_date_range(start_date: str, end_date: str) -> None:
    today = date.today()
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    if end < start:
        raise ValueError("종료 날짜는 시작 날짜보다 빠를 수 없습니다.")

    max_date = today + timedelta(days=MAX_FORECAST_DAYS - 1)
    if start > max_date or end > max_date:
        raise ValueError(
            f"{start_date}~{end_date}에 대한 예보 데이터가 없습니다. "
            f"(Open-Meteo는 오늘로부터 최대 {MAX_FORECAST_DAYS}일 이내 예보만 제공합니다)"
        )


def get_weather_for_period(lat: float, lon: float, start_date: str, end_date: str) -> list:
    """Open-Meteo 일별 예보에서 start_date~end_date('YYYY-MM-DD') 구간의
    날짜별 날씨 요약 리스트를 반환한다.

    무료 API는 최대 16일 이내 예보만 제공하므로, 그 이후 날짜는 ValueError를 던진다.
    """
    _validate_date_range(start_date, end_date)

    resp = requests.get(
        FORECAST_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "daily": (
                "weathercode,temperature_2m_max,temperature_2m_min,"
                "precipitation_probability_max,windspeed_10m_max,relative_humidity_2m_mean"
            ),
            "timezone": "Asia/Seoul",
            "start_date": start_date,
            "end_date": end_date,
        },
        timeout=5,
    )
    resp.raise_for_status()
    daily = resp.json()["daily"]

    results = []
    for i, day in enumerate(daily["time"]):
        temp_max = round(daily["temperature_2m_max"][i], 1)
        pop = round(daily["precipitation_probability_max"][i])
        windspeed = round(daily["windspeed_10m_max"][i] / 3.6, 1)  # km/h -> m/s
        humidity = round(daily["relative_humidity_2m_mean"][i])

        results.append(
            {
                "date": day,
                "condition": _describe_weather_code(daily["weathercode"][i]),
                "temp_min": round(daily["temperature_2m_min"][i], 1),
                "temp_max": temp_max,
                "pop": pop,
                "windspeed": windspeed,
                "humidity": humidity,
                "travel_index": _travel_index(temp_max, pop, daily["windspeed_10m_max"][i], humidity),
            }
        )

    if not results:
        raise ValueError(f"{start_date}~{end_date}에 대한 예보 데이터가 없습니다.")

    return results


def get_weather_for_date(lat: float, lon: float, target_date: str) -> dict:
    """단일 날짜 조회 (하위 호환용). get_weather_for_period의 결과 중 첫 항목을 반환한다."""
    return get_weather_for_period(lat, lon, target_date, target_date)[0]
