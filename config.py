# =============================
# 設定（サイズ・色・難易度）
# =============================
WIDTH, HEIGHT = 480, 640

PLAYER_SIZE = 40
PLAYER_SPEED = 6

ENEMY_SIZE = 40
ENEMY_COLOR = (255, 80, 80)
ENEMY_BASE_SPEED = 4.0
NUM_ENEMIES = 3

# 当たり判定を少し小さく（1.0で無効）
HITBOX_SHRINK = 0.85

# 見た目サイズ（画像のスケール）
PLAYER_VISUAL_SIZE = (PLAYER_SIZE, PLAYER_SIZE)
ENEMY_VISUAL_SIZE  = (ENEMY_SIZE, ENEMY_SIZE)

# サウンド設定
BGM_VOLUME = 0.4
SFX_VOLUME = 0.8
MUTED = False

# アセットのパス
PLAYER_PATH = "assets/player.png"
ENEMY_PATH  = "assets/enemy.png"
BG_PATH     = "assets/bg.png"
BGM_PATH    = "assets/bgm.mp3"
HIT_PATH    = "assets/hit.wav"
START_PATH  = "assets/start.wav"

# Project version
VERSION = "v0.2"
