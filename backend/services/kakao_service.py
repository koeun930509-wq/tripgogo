import os

import requests

ADDRESS_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/address.json"
KEYWORD_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"


def geocode_region(region: str) -> dict:
    """지역명을 카카오맵 API로 위도/경도로 변환한다.

    주소 검색으로 못 찾으면(예: '제주도', '해운대'처럼 정식 주소가 아닌 지역명)
    키워드 검색으로 한 번 더 시도한다.
    """
    api_key = os.environ["KAKAO_REST_API_KEY"]
    headers = {"Authorization": f"KakaoAK {api_key}"}

    documents = _search(ADDRESS_SEARCH_URL, headers, region)
    if not documents:
        documents = _search(KEYWORD_SEARCH_URL, headers, region)

    if not documents:
        raise ValueError(f"'{region}'에 대한 위치 정보를 찾을 수 없습니다.")

    doc = documents[0]
    return {
        "lat": float(doc["y"]),
        "lon": float(doc["x"]),
        "matched_name": doc.get("address_name") or doc.get("place_name"),
    }


def _search(url: str, headers: dict, query: str) -> list:
    resp = requests.get(url, headers=headers, params={"query": query}, timeout=5)
    resp.raise_for_status()
    return resp.json().get("documents", [])
