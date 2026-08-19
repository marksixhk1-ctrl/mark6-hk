import json
import requests

def get_hkjc_mark6():
    # 使用專為開放資料設計的穩定 API 介面
    url = "https://a.mark-six.com/api/latest"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            result = {
                "period": str(data.get("period", "最新期數")),
                "date": str(data.get("date", "開獎日")),
                "numbers": data.get("numbers", [])
            }
        else:
            raise Exception(f"HTTP Error {response.status_code}")
            
    except Exception as e:
        # 備用方案：馬會備用靜態數據源
        print(f"主要來源失敗，切換備用源: {e}")
        url_backup = "https://bet.hkjc.com/contentserver/jcw/cms/marksix/results/en/last_draw.json"
        res = requests.get(url_backup, headers=headers, timeout=10)
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
                "code": f"特別號: {str(sp.get('number')).zfill(2)}",
                "color": str(sp.get("colour", "red")).lower()
            })
            
        result = {
            "period": data.get("drawId", ""),
            "date": data.get("drawDate", ""),
            "numbers": drawn
        }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print("數據讀取與寫入成功！")

if __name__ == "__main__":
    get_hkjc_mark6()
