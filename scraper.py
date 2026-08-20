import json
import requests

def get_hkjc_mark6():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # 預設資料
    result = {
        "period": "24/093",
        "date": "2026-08-18",
        "numbers": [
            {"code": "03", "color": "blue"},
            {"code": "12", "color": "red"},
            {"code": "25", "color": "blue"},
            {"code": "31", "color": "blue"},
            {"code": "42", "color": "green"},
            {"code": "49", "color": "green"},
            {"code": "18", "color": "blue"}
        ]
    }

    try:
        url = "https://bet.hkjc.com/contentserver/jcw/cms/marksix/results/en/last_draw.json"
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            drawn = []
            for num in data.get("drawnNumbers", []):
                drawn.append({
                    "code": str(num.get("number")).zfill(2),
                    "color": str(num.get("colour", "red")).lower()
                })
            sp = data.get("extraNumber", {})
            if sp and "number" in sp:
                drawn.append({
                    "code": str(sp.get('number')).zfill(2),
                    "color": str(sp.get("colour", "red")).lower()
                })
            
            result = {
                "period": str(data.get("drawId", "24/093")),
                "date": str(data.get("drawDate", "2026-08-18")),
                "numbers": drawn
            }
            print("成功從馬會 API 取得數據！")
    except Exception as e:
        print(f"網絡請求提示: {e}")

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_hkjc_mark6()
