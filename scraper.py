import json
import requests

def get_hkjc_mark6():
    # 馬會官方六合彩最新結果 API 網址
    url = "https://bet.hkjc.com/contentserver/jcw/cms/marksix/results/en/last_draw.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # 提取期數與日期
        draw_id = data.get("drawId", "")
        draw_date = data.get("drawDate", "")
        
        # 提取號碼與波色
        drawn_numbers = []
        for num in data.get("drawnNumbers", []):
            drawn_numbers.append({
                "code": str(num.get("number")).zfill(2),
                "color": str(num.get("colour")).lower()
            })
        
        # 提取特別號碼
        special_num = data.get("extraNumber", {})
        if special_num:
            drawn_numbers.append({
                "code": f"特別號: {str(special_num.get('number')).zfill(2)}",
                "color": str(special_num.get("colour")).lower()
            })
        
        result = {
            "period": draw_id,
            "date": draw_date,
            "numbers": drawn_numbers
        }
        
        # 寫入 data.json 供前端讀取
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        print("成功抓取馬會最新數據並更新 data.json！")
        
    except Exception as e:
        print(f"抓取數據失敗: {e}")
        raise e

if __name__ == "__main__":
    get_hkjc_mark6()
