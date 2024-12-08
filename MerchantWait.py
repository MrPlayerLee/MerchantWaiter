from datetime import datetime, timedelta
import time
from pydub.generators import Sine
import simpleaudio as sa
import os

# 비프음 생성 함수
def generate_beep():
    sound = Sine(1400).to_audio_segment(duration=100)
    playback = sa.play_buffer(
        sound.raw_data,
        num_channels=1,
        bytes_per_sample=2,
        sample_rate=44100
    )
    playback.wait_done()

# 반복 알람 설정 함수
def set_repeating_alarm():
    HowMuchTime = int(1800)                                             # 여기서 기초 시간 변경

    while True:
        now = datetime.now()
        next_alarm_time = now + timedelta(seconds=HowMuchTime)
        os.system('cls' if os.name == 'nt' else 'clear')  # 콘솔 화면 지우기
        print(f"반복 알람이 {HowMuchTime}초 간격으로 울립니다.")
        print(f"현재 시간: {now.strftime('%H:%M:%S')}")
        print(f"다음 알람 시간: {next_alarm_time.strftime('%H:%M:%S')}")

        while datetime.now() < next_alarm_time:
            current_time = datetime.now()
            remaining_time = next_alarm_time - current_time
            minutes, seconds = divmod(remaining_time.seconds, 60)
            hours = remaining_time.seconds // 3600

            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"남은 시간: {hours:02}:{minutes:02}:{seconds:02}")
            print(f"다음 작살아귀 시간: {next_alarm_time.strftime('%H:%M:%S')}")

            # 현실시간에 맞게 보정
            time_to_sleep = 1.0 - (datetime.now() - current_time).total_seconds()
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)

        # 알람 부분
        os.system('cls' if os.name == 'nt' else 'clear')
        #print("상선 왔다!!!!") # 이걸 꼭 넣어야할까
        generate_beep()

# 반복 알람 실행
generate_beep()
set_repeating_alarm()
