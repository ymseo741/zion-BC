import json
import random
import math
from datetime import datetime, timedelta

# 기준 좌표 (국동항 앞 바다)
BASE_LON = 127.7617
BASE_LAT = 34.7808

ONE_DEG_LAT = 111_000
ONE_DEG_LON = ONE_DEG_LAT * math.cos(math.radians(BASE_LAT))

start_dt = datetime(2025,6,10,0,0,0)
interval = timedelta(seconds=10)
num_points = 12*60*60//10  # 4320 시점

gateway_id = "GW-국동항-01"
num_beacons = 10

all_data = []

# 각 비콘별 50개의 간헐적 gap 생성 (2~20분)
beacon_gaps = {}
for bidx in range(1, num_beacons+1):
    gaps = []
    used = set()
    for _ in range(50):
        # gap 시작점이 겹치지 않게(충돌 방지)
        while True:
            gap_start = random.randint(0, num_points-120)
            overlap = any(not (gap_start+random.randint(12,120) < s or gap_start > e) for (s,e) in gaps)
            if not overlap:
                break
        gap_duration = random.randint(12, 120)  # 2~20분 (10초 단위)
        gaps.append( (gap_start, gap_start+gap_duration) )
    beacon_gaps[f"BC-국동항-{bidx:02d}"] = gaps

for i in range(num_points):
    dt = start_dt + i*interval
    # 게이트웨이(고정)
    gateway = {
        "device_id": gateway_id,
        "coordinates": [BASE_LON, BASE_LAT],  # [경도, 위도]
        "unit": "GPS",
        "measure_time": dt.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "value": None
    }
    all_data.append(gateway)
    # 비콘 10개
    for bidx in range(1, num_beacons+1):
        beacon_id = f"BC-국동항-{bidx:02d}"
        # gap 구간인지 확인
        in_gap = False
        for (start, end) in beacon_gaps[beacon_id]:
            if start <= i <= end:
                in_gap = True
                break
        if in_gap:
            continue
        # 5~10m 거리 난수, 각자 독립적으로 랜덤 이동
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(5, 10)
        east = distance * math.cos(angle)
        north = distance * math.sin(angle)
        lon = BASE_LON + (east / ONE_DEG_LON)
        lat = BASE_LAT + (north / ONE_DEG_LAT)
        beacon = {
            "device_id": beacon_id,
            "coordinates": [round(lon,8), round(lat,8)],  # [경도, 위도]
            "unit": "BLE",
            "measure_time": dt.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "value": None
        }
        all_data.append(beacon)

# JSON 파일 저장
with open("yeosu_gukdong_ble_5to10m_50gaps.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"생성 완료: yeosu_gukdong_ble_5to10m_50gaps.json (총 {len(all_data)}건)")
