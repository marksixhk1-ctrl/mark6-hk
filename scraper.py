import json

def fetch_mark6():
    # 示範資料結構（含號碼與對應波色）
    result = {
        "period": "24/080",
        "date": "2026-08-18",
        "numbers": [
            {"code": "01", "color": "red"},
            {"code": "12", "color": "red"},
            {"code": "24", "color": "green"},
            {"code": "33", "color": "green"},
            {"code": "41", "color": "blue"},
            {"code": "48", "color": "blue"},
            {"code": "特別號: 06", "color": "green"}
        ]
    }
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_mark6()
