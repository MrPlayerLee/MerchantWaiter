import sys
import os
from datetime import datetime, timedelta
import time
from pydub.generators import Sine
import simpleaudio as sa

# 콘솔 인코딩 설정
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
else:
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

# 알람용 비프음 생성
def generate_beep():
    sound = Sine(1400).to_audio_segment(duration=100)
    playback = sa.play_buffer(
        sound.raw_data,
        num_channels=1,
        bytes_per_sample=2,
        sample_rate=44100
    )
    playback.wait_done()

# 다음 이벤트 시간 계산. 00시 15분 00초 기준.
def calculate_next_event():
    now = datetime.now()
    base_time = now.replace(hour=0, minute=15, second=0, microsecond=0)

    if now < base_time:
        return base_time

    time_since_base = (now - base_time).total_seconds()
    next_event_offset = (30 * 60) - (time_since_base % (30 * 60))
    return now + timedelta(seconds=next_event_offset)

# 무한 반복으로 알람 실행
def set_repeating_alarm():
    previous_remaining_time = None
    while True:
        next_event_time = calculate_next_event()
        while True:
            now = datetime.now()
            remaining_time = (next_event_time - now).total_seconds()

            if remaining_time <= 0:
                break

            if previous_remaining_time != int(remaining_time):
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"다음 상선 시간: {next_event_time.strftime('%H : %M')}")
                print(f"남은 시간: {int(remaining_time // 60)} : {int(remaining_time % 60)}")
                previous_remaining_time = int(remaining_time)

            time.sleep(0.1)

        # 첫 번째 알람
        generate_beep()

        # 상선 건너오는 시간(35초) 대기 후 실시간 갱신
        for i in range(35):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("상선 건너오기 대기 중...")
            print(f"남은 시간: {35 - i}초")
            time.sleep(1)

        # 두 번째 알람
        generate_beep()

# 메인 루프 코드 실행
set_repeating_alarm()
