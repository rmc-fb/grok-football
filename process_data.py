import json
from datetime import datetime, timedelta
import sys

def clean_old_matches():
    input_file = 'data/matches.json'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            matches = json.load(f)
    except FileNotFoundError:
        print("データファイルが見つかりません")
        return
    except json.JSONDecodeError:
        print("JSONの形式が壊れています")
        return

    now = datetime.utcnow()
    threshold = now - timedelta(hours=2)  # キックオフから2時間後

    cleaned = []
    kept_count = 0

    for match in matches:
        try:
            # 実際のJSONキー名に合わせて調整（後で直す）
            time_field = match.get('startTime') or match.get('timestamp') or match.get('time') or match.get('start')
            
            if time_field:
                # ISO形式の日時をパース
                if isinstance(time_field, str):
                    match_time = datetime.fromisoformat(time_field.replace('Z', '+00:00'))
                else:
                    match_time = datetime.fromtimestamp(time_field)
                
                if match_time > threshold:
                    cleaned.append(match)
                    kept_count += 1
        except:
            # 日時パースに失敗した試合は一旦残す（安全策）
            cleaned.append(match)
            kept_count += 1

    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"クリーニング完了: {len(matches)}件 → {kept_count}件 に削減")

if __name__ == "__main__":
    clean_old_matches()