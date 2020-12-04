import time


def animated_print(text: str) -> None:
    for obj in text:
        time.sleep(0.03)
        print(obj, sep=' ', end='', flush=True)
