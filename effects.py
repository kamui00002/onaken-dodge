# =============================
# 揺れ（スクリーンシェイク）
# =============================
import random

SHAKE_TIME_LEFT = 0
SHAKE_MAGNITUDE = 0

def apply_shake(duration_ms=300, magnitude_px=8):
    global SHAKE_TIME_LEFT, SHAKE_MAGNITUDE
    SHAKE_TIME_LEFT = duration_ms
    SHAKE_MAGNITUDE = magnitude_px

def update_shake(dt_ms):
    global SHAKE_TIME_LEFT
    if SHAKE_TIME_LEFT > 0:
        SHAKE_TIME_LEFT = max(0, SHAKE_TIME_LEFT - dt_ms)

def get_shake_offset():
    if SHAKE_TIME_LEFT <= 0:
        return (0, 0)
    return (
        random.randint(-SHAKE_MAGNITUDE, SHAKE_MAGNITUDE),
        random.randint(-SHAKE_MAGNITUDE, SHAKE_MAGNITUDE),
    )
