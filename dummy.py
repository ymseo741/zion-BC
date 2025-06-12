import json
import random
import math
from datetime import datetime, timedelta

# 기준 좌표(첨부 파일 기준)
base_lon = 126.62715148925781
base_lat = 34.15813064575195

# 위도/경도 1도당 미터 환산
one_deg_lat = 111_000
one_deg_lon = 111_000 * math.cos(base_lat * math.pi / 180)

# 5분 간격 12시간 = 145개
start_dt = datetime(2025,6,10,0,0,0)
interval = timedelta(minutes=5)
num_points = 12*60//5 + 1

# 각 디바이스별로 범위(반경 100m) 내에서 난수 이동
RADIUS_M = 100  # 최대 반경(m)

for idx in range(1, 11):
    device_id = f"gis{idx:02d}"
    data = []
    for i in range(num_points):
        dt = start_dt + i*interval
        # 난수 각도/거리
        angle = random.uniform(0, 2*math.pi)
        dist = random.uniform(0, RADIUS_M)
        # 디바이스별로 중심값을 약간씩 다르게(서로 겹치지 않게)
        center_east = 15*idx
        center_north = 15*idx
        # 실제 위치 계산
        east = center_east + dist * math.cos(angle)
        north = center_north + dist * math.sin(angle)
        lon = base_lon + east / one_deg_lon
        lat = base_lat + north / one_deg_lat
        # 더미 수온값(16~20도에서 약간의 노이즈)
        value = 18 + math.sin(i/10.0 + idx) + (idx-5)*0.1 + random.uniform(-0.5,0.5)
        data.append({
            "coordinates": [round(lon,8), round(lat,8)],
            "unit": "°C",
            "device_id": device_id,
            "measure_time": dt.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "value": round(value, 3)
        })
    fname = f"{device_id}_temp_20250610_0000_20250610_1155.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"저장 완료: {fname} ({len(data)}개 데이터)")
