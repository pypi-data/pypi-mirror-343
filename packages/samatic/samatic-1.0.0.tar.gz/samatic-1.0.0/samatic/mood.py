import os
import time

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def mood_booster():
    print("Boosting your mood... 🚀\n")
    time.sleep(1)

    frames = [
        r"\o/",
        r" o/",
        r"\o ",
        r" o ",
    ]
    for _ in range(10):  # Repeat 10 times
        for frame in frames:
            clear_console()
            print(frame)
            print("Shake it! 💃🕺")
            time.sleep(0.3)

if __name__ == "__main__":
    mood_booster()
