# make_hit.py
import pygame
import numpy as np
import os

os.makedirs("assets", exist_ok=True)
pygame.mixer.init(frequency=44100, size=-16, channels=1)

def generate_tone(filename, freq=220, duration=0.4, volume=0.6):
    """低めのドンという効果音を生成"""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(freq * t * 2 * np.pi)
    # 波形を少し減衰させてドンっぽくする
    wave *= np.exp(-3 * t)
    audio = (wave * (2**15 - 1) * volume).astype(np.int16)
    sound = pygame.sndarray.make_sound(audio)
    pygame.mixer.Sound.save(sound, filename)
    print("saved:", filename)

# ヒット音を保存
generate_tone("assets/hit.wav")

pygame.quit()
