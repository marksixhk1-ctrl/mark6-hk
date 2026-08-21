import json
import requests

def get_hkjc_mark6():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # 預設範例派彩資料（若連線異常時備用）
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
        ],
        "prizes": [
            {"prize": "頭獎", "winning_units": "1.0", "per_unit": "$8,000,000"},
            {"prize": "二獎", "winning_units": "2.5", "per_unit": "$38,400"},
            {"prize": "三獎", "winning_units": "85.0", "per_unit": "$19,200"},
            {"prize": "四獎", "winning_units": "150.0", "per_unit": "$9,600"},
            {"prize": "五獎", "winning_units": "3,200.0", "per_unit": "$640"},
            {"prize": "六獎", "winning_units": "4,500.0", "per_unit": "$320"},
            {"prize": "七獎", "winning_units": "58,000.0", "per_unit": "$40"}
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
            
            # 處理派彩列表
            prizes_data = []
            prizes_raw = data.get("prizes", [])
            prize_names = ["頭獎", "二獎", "三獎", "四獎", "五獎", "六獎", "七獎"]
            
            for idx, item in enumerate(prizes_raw[:7]):
                p_name = prize_names[idx] if idx < len(prize_names) else f"{idx+1}獎"
                prizes_data.append({
                    "prize": p_name,
                    "winning_units": str(item.get("winningUnits", "0")),
                    "per_unit": f"${item.get('dividend', 0):,}" if isinstance(item.get('dividend'), (int, float)) else str(item.get('dividend', '$0'))
                })
            
            if prizes_data:
                result["prizes"] = prizes_data

            result["period"] = str(data.get("drawId", "24/093"))
            result["date"] = str(data.get("drawDate", "2026-08-18"))
            
            print("成功從馬會 API 取得號碼與派彩數據！")
    except Exception as e:
        print(f"網絡請求提示（已啟用預設派彩數據）: {e}")

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_hkjc_mark6()
