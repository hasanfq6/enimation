from enimation import loading, list_animations
from enimation.motions import *
import time

list_animations()

@loading(custom=wave_animation)
def long_task():
    time.sleep(5)

long_task()
