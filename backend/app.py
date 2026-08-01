from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify, request
from flask_cors import CORS

from pipeline import get_travel_recommendation

app = Flask(__name__)
CORS(app)


@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json(silent=True) or {}
    region = (data.get("region") or "").strip()
    date = (data.get("date") or "").strip()
    end_date = (data.get("endDate") or "").strip() or None

    if not region or not date:
        return jsonify({"error": "region과 date는 필수입니다."}), 400

    try:
        result = get_travel_recommendation(region, date, end_date)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "추천 생성 중 오류가 발생했습니다.", "detail": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
