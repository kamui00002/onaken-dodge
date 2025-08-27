# =============================
# 画像・音のロードと描画ユーティリティ
# =============================
import os
import pygame
import config

# モジュール内で共有するリソース
player_img = None
enemy_img  = None
bg_img     = None
start_snd  = None
hit_snd    = None

def _load_image(path, size=None):
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        if size is not None:
            img = pygame.transform.smoothscale(img, size)
        return img
    return None

def _ensure_hit_sound(path=config.HIT_PATH):
    """hit.wav が無い時だけ自動生成（numpy不要・遅延import）"""
    if os.path.exists(path):
        return
    try:
        import wave, numpy as np
        sample_rate = 44100
        duration = 0.45
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        base = np.sin(190 * 2*np.pi * t)
        harm = 0.4 * np.sin(380 * 2*np.pi * t)
        noise = 0.15 * (np.random.rand(len(t)) * 2 - 1)
        wave_mono = (base + harm + noise)
        env = np.exp(-4.0 * t)
        wave_mono *= env
        wave_mono = wave_mono / np.max(np.abs(wave_mono))
        audio_i16 = (wave_mono * (2**15 - 1) * 0.9).astype(np.int16)
        with wave.open(path, "wb") as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sample_rate)
            wf.writeframes(audio_i16.tobytes())
    except Exception as e:
        print("hit.wav 自動生成に失敗:", e)

def _load_sound_safe(path, volume=0.8):
    if os.path.exists(path):
        try:
            snd = pygame.mixer.Sound(path)
            snd.set_volume(volume)
            return snd
        except pygame.error as e:
            print("サウンド読み込み失敗:", path, e)
    return None

def init_assets():
    """画像・音のロード。pygame.init 後に一度だけ呼ぶ"""
    global player_img, enemy_img, bg_img, start_snd, hit_snd
    player_img = _load_image(config.PLAYER_PATH, config.PLAYER_VISUAL_SIZE)
    enemy_img  = _load_image(config.ENEMY_PATH,  config.ENEMY_VISUAL_SIZE)
    bg_img     = _load_image(config.BG_PATH,     (config.WIDTH, config.HEIGHT))

    _ensure_hit_sound(config.HIT_PATH)
    start_snd = _load_sound_safe(config.START_PATH, volume=config.SFX_VOLUME)
    hit_snd   = _load_sound_safe(config.HIT_PATH,   volume=0.95)

def draw_background(screen, offset=(0, 0)):
    ox, oy = offset
    if bg_img:
        screen.blit(bg_img, (ox, oy))
    else:
        screen.fill((0, 0, 0))

def draw_with_shadow(screen, surface, x, y, shadow_offset=(4, 4), shadow_color=(0, 0, 0, 100)):
    if surface:
        shadow = surface.copy()
        shadow.fill(shadow_color, special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(shadow, (x + shadow_offset[0], y + shadow_offset[1]))
        screen.blit(surface, (x, y))
    else:
        # フォールバックで白四角＋影
        import pygame as _pg
        shadow_rect = _pg.Rect(x + shadow_offset[0], y + shadow_offset[1],
                               config.PLAYER_SIZE, config.PLAYER_SIZE)
        _pg.draw.rect(screen, (50, 50, 50), shadow_rect)
        rect = _pg.Rect(x, y, config.PLAYER_SIZE, config.PLAYER_SIZE)
        _pg.draw.rect(screen, (255, 255, 255), rect)

def start_bgm(loop=-1):
    if os.path.exists(config.BGM_PATH):
        try:
            pygame.mixer.music.load(config.BGM_PATH)
            pygame.mixer.music.set_volume(config.BGM_VOLUME if not config.MUTED else 0.0)
            pygame.mixer.music.play(loop)
        except pygame.error as e:
            print("BGM読み込み/再生失敗:", e)

def apply_volumes():
    vol = 0.0 if config.MUTED else 1.0
    try:
        pygame.mixer.music.set_volume(config.BGM_VOLUME * vol)
    except Exception:
        pass
    if start_snd: start_snd.set_volume(config.SFX_VOLUME * vol)
    if hit_snd:   hit_snd.set_volume(config.SFX_VOLUME * vol)
