import time
import random

messages = [
    "Hello, World! 🌍",
    "안녕, 세상아! 👋",
    "야 일어나! 코딩할 시간이야! 💻",
    "오늘도 버그 없는 하루 되세요 🙏",
    "Python 최고! ❤️",
]

print("=" * 40)
print("  부팅 중...")
time.sleep(0.5)

for i in range(1, 4):
    print(f"  로딩 {'.' * i}", end="\r")
    time.sleep(0.4)

print("\n" + "=" * 40)
print(f"\n  >> {random.choice(messages)}\n")
print("=" * 40)
