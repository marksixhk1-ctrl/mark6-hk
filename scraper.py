import json
import requests

def get_hkjc_mark6():
    url = "https://bet.hkjc.com/contentserver/jcw/cms/marksix/results/en/last_draw.json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://bet.hkjc.com/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        draw_id = data.get("drawId", "")
        draw_date = data.get("drawDate", "")
        
        drawn_numbers = []
        for num in data.get("drawnNumbers", []):
            drawn_numbers.append({
                "code": str(num.get("number")).zfill(2),
                "color": str(num.get("colour", "")).lower()
            })
        
        special_num = data.get("extraNumber", {})
        if special_num and "number" in special_num:
            drawn_numbers.append({
                "code": f"特別號: {str(special_num.get('number')).zfill(2)}",
                "color": str(special_num.get("colour", "")).lower()
            })
        
        result = {
            "period": draw_id,
            "date": draw_date,
            "numbers": drawn_numbers
        }
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        print("數據抓取成功！")
        
    except Exception as e:
        print(f"錯誤細節: {e}")
        # 若 API 失敗，產出備用基本資料避免工作流程完全崩潰
        fallback = {
            "period": "最新期數",
            "date": "開獎日",
            "numbers": [{"code": "00", "color": "red"}]
        }
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(fallback, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_hkjc_mark6()
