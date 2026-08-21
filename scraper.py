import json
import requests

def get_hkjc_mark6():
    url = "https://bet.hkjc.com/contentserver/jcw/cms/marksix/results/en/last_draw.json"
    
    # 完整模擬瀏覽器 Header，防止被馬會伺服器阻擋
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://bet.hkjc.com/marksix/index.aspx?lang=ch",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    # 預設結構
    result = {
        "period": "",
        "date": "",
        "numbers": [],
        "prizes": []
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()
        
        # 處理攪珠號碼
        drawn = []
        for num in data.get("drawnNumbers", []):
            drawn.append({
                "code": str(num.get("number")).zfill(2),
                "color": str(num.get("colour", "red")).lower()
            })
        
        # 處理特別號
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
            div = item.get('dividend', 0)
            div_str = f"${div:,.0f}" if isinstance(div, (int, float)) else str(div)
            
            prizes_data.append({
                "prize": p_name,
                "winning_units": str(item.get("winningUnits", "0")),
                "per_unit": div_str
            })

        result["period"] = str(data.get("id", data.get("drawId", "最新期數")))
        result["date"] = str(data.get("date", data.get("drawDate", "")))
        result["numbers"] = drawn
        result["prizes"] = prizes_data
        
        print(f"成功抓取最新期數：{result['period']} ({result['date']})")

    except Exception as e:
        print(f"抓取失敗，錯誤資訊: {e}")

    # 將數據寫入 data.json
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_hkjc_mark6()
