import json
import re
import pandas as pd
import numpy as np

def _fix_decimal_separator(s: str) -> str:
    return s.replace(',', '.')

def _parse_pose_string(pose_str: str) -> list:
   
    if not pose_str:
        return []
    numbers = re.findall(r'[-+]?\d*[.,]\d+|[-+]?\d+', pose_str)
    return [float(_fix_decimal_separator(n)) for n in numbers]

def load_tracking_data(filepath: str) -> pd.DataFrame:

    records = []
    first_line_data = None

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
)
            if 'notice' in data:
                first_line_data = data
                continue

            record = {}

            if 'predictTime' in data:
                record['time'] = data['predictTime']
            else:
                record['time'] = None

            head = data.get('Head', {})
            head_pose_str = head.get('pose', '')
            head_pose = _parse_pose_string(head_pose_str)
            if len(head_pose) >= 7:
                record['head_x'] = head_pose[0]
                record['head_y'] = head_pose[1]
                record['head_z'] = head_pose[2]
                record['head_qx'] = head_pose[3]
                record['head_qy'] = head_pose[4]
                record['head_qz'] = head_pose[5]
                record['head_qw'] = head_pose[6]

            hand = data.get('Hand', {})
            for side, key in [('left', 'leftHand'), ('right', 'rightHand')]:
                hand_data = hand.get(key, {})
                if hand_data.get('isActive', 0) == 1:
                    joints = hand_data.get('HandJointLocations', [])
                    if joints:
                        wrist_pose_str = joints[0].get('p', '')
                        wrist_pose = _parse_pose_string(wrist_pose_str)
                        if len(wrist_pose) >= 3:
                            record[f'{side}_wrist_x'] = wrist_pose[0]
                            record[f'{side}_wrist_y'] = wrist_pose[1]
                            record[f'{side}_wrist_z'] = wrist_pose[2]

            records.append(record)

    df = pd.DataFrame(records)

    if 'time' in df.columns:
        df = df.dropna(subset=['time'])
        df = df.sort_values('time').reset_index(drop=True)

    return df, first_line_data


if __name__ == '__main__':
    df, camera_info = load_tracking_data('data/trackingData_20260505_165740.txt')
    print(f"Загружено кадров: {len(df)}")
    print(f"Колонки: {list(df.columns)}")
    print(df.head())
    print(f"\nДлительность: {df['time'].max() - df['time'].min():.2f} секунд")
    print(f"Средняя частота: {len(df) / (df['time'].max() - df['time'].min()):.1f} Гц")