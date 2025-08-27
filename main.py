import sys, os, pygame, random
import config
import effects
import assets

# -----------------------------
# 初期化
# -----------------------------
pygame.init()
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2)
except pygame.error:
    pass

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("ONAKEN DODGE")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# アセット読み込み
assets.init_assets()

# -----------------------------
# ゲーム状態
# -----------------------------
STATE = "TITLE"   # "TITLE" / "PLAYING" / "GAMEOVER"
score = 0

# プレイヤー
player_x = config.WIDTH // 2 - config.PLAYER_SIZE // 2
player_y = config.HEIGHT - config.PLAYER_SIZE - 20

# 敵たち
enemies = []

def reset_game():
    global score, player_x, player_y, enemies
    score = 0
    player_x = config.WIDTH // 2 - config.PLAYER_SIZE // 2
    player_y = config.HEIGHT - config.PLAYER_SIZE - 20
    enemies = []
    for _ in range(config.NUM_ENEMIES):
        enemies.append({
            "x": random.randint(0, config.WIDTH - config.ENEMY_SIZE),
            "y": random.randint(-config.HEIGHT, -config.ENEMY_SIZE),
            "speed": config.ENEMY_BASE_SPEED
        })

reset_game()

def draw_volume_ui():
    """右上に MUTE / VOL % を表示"""
    label = "MUTE" if config.MUTED else f"VOL {int(config.BGM_VOLUME*100)}%"
    surf = font.render(label, True, (180,180,180))
    w, h = surf.get_size()
    screen.blit(surf, (config.WIDTH - w - 10, 10))

# -----------------------------
# メインループ
# -----------------------------
running = True
while running:
    dt_ms = clock.tick(60)
    effects.update_shake(dt_ms)
    sx, sy = effects.get_shake_offset()

    # イベント
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # 音量操作：[ / ] と M
            if event.key == pygame.K_LEFTBRACKET:   # [
                config.BGM_VOLUME = max(0.0, round(config.BGM_VOLUME - 0.05, 2))
                config.SFX_VOLUME = max(0.0, round(config.SFX_VOLUME - 0.05, 2))
                assets.apply_volumes()
            elif event.key == pygame.K_RIGHTBRACKET: # ]
                config.BGM_VOLUME = min(1.0, round(config.BGM_VOLUME + 0.05, 2))
                config.SFX_VOLUME = min(1.0, round(config.SFX_VOLUME + 0.05, 2))
                assets.apply_volumes()
            elif event.key == pygame.K_m:            # Mute toggle
                config.MUTED = not config.MUTED
                assets.apply_volumes()

    # === TITLE ===
    if STATE == "TITLE":
        assets.draw_background(screen, (0, 0))

        title_text = "ONAKEN DODGE"
        colors = [(255,80,80),(255,180,80),(255,255,80),
                  (80,255,80),(80,180,255),(180,80,255)]
        title_font = pygame.font.SysFont(None, 64)
        x_offset = config.WIDTH // 2 - len(title_text) * 16
        for i, ch in enumerate(title_text):
            ch_surf = title_font.render(ch, True, colors[i % len(colors)])
            screen.blit(ch_surf, (x_offset + i * 32, config.HEIGHT // 2 - 70))

        tip = font.render("Press SPACE to Start", True, (150, 150, 150))
        screen.blit(tip, tip.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 + 50)))

        # 音量UI（右上）
        draw_volume_ui()

        if not pygame.mixer.music.get_busy():
            assets.start_bgm(loop=-1)

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            reset_game()
            STATE = "PLAYING"
            if assets.start_snd:
                assets.start_snd.play()
        continue

    # === PLAYING ===
    if STATE == "PLAYING":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  player_x -= config.PLAYER_SPEED
        if keys[pygame.K_RIGHT]: player_x += config.PLAYER_SPEED
        player_x = max(0, min(player_x, config.WIDTH - config.PLAYER_SIZE))

        # 敵落下
        for e in enemies:
            e["y"] += e["speed"]
            if e["y"] > config.HEIGHT:
                e["y"] = -config.ENEMY_SIZE
                e["x"] = random.randint(0, config.WIDTH - config.ENEMY_SIZE)

        # 当たり判定（縮小）
        player_rect = pygame.Rect(player_x, player_y, config.PLAYER_SIZE, config.PLAYER_SIZE)
        if config.HITBOX_SHRINK != 1.0:
            pw = int(player_rect.width * config.HITBOX_SHRINK)
            ph = int(player_rect.height * config.HITBOX_SHRINK)
            player_rect = pygame.Rect(0, 0, pw, ph)
            player_rect.center = (player_x + config.PLAYER_SIZE // 2,
                                  player_y + config.PLAYER_SIZE // 2)

        hit = False
        for e in enemies:
            enemy_rect = pygame.Rect(e["x"], e["y"], config.ENEMY_SIZE, config.ENEMY_SIZE)
            if config.HITBOX_SHRINK != 1.0:
                ew = int(enemy_rect.width * config.HITBOX_SHRINK)
                eh = int(enemy_rect.height * config.HITBOX_SHRINK)
                enemy_rect = pygame.Rect(0, 0, ew, eh)
                enemy_rect.center = (e["x"] + config.ENEMY_SIZE // 2,
                                     e["y"] + config.ENEMY_SIZE // 2)
            if player_rect.colliderect(enemy_rect):
                hit = True
                break

        if hit:
            effects.apply_shake(duration_ms=350, magnitude_px=9)
            if assets.hit_snd:
                assets.hit_snd.play()
            STATE = "GAMEOVER"

        if STATE == "PLAYING":
            score += 1
            if score % 180 == 0:
                for e in enemies:
                    e["speed"] += 0.5

        # 描画（揺れを適用）
        assets.draw_background(screen, (0, 0))
        assets.draw_with_shadow(screen, assets.player_img, player_x + sx, player_y + sy)
        for e in enemies:
            if assets.enemy_img:
                assets.draw_with_shadow(screen, assets.enemy_img, e["x"] + sx, e["y"] + sy)
            else:
                pygame.draw.rect(screen, config.ENEMY_COLOR,
                                 (e["x"] + sx, e["y"] + sy, config.ENEMY_SIZE, config.ENEMY_SIZE))

        score_surf = font.render(f"Score: {score}", True, (200, 200, 200))
        screen.blit(score_surf, (10 + sx, 10 + sy))

        # 音量UI
        draw_volume_ui()

        pygame.display.flip()
        continue

    # === GAMEOVER ===
    if STATE == "GAMEOVER":
        sx, sy = effects.get_shake_offset()
        assets.draw_background(screen, (0, 0))
        big_font = pygame.font.SysFont(None, 48)
        text = big_font.render("GAME OVER", True, (255, 80, 80))
        screen.blit(text, text.get_rect(center=(config.WIDTH // 2 + sx, config.HEIGHT // 2 - 40 + sy)))
        tip = font.render("Press R to Retry or Q to Quit", True, (170, 170, 170))
        screen.blit(tip, tip.get_rect(center=(config.WIDTH // 2 + sx, config.HEIGHT // 2 + 20 + sy)))

        # 音量UI
        draw_volume_ui()

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()
            STATE = "PLAYING"
            if assets.start_snd:
                assets.start_snd.play()
        elif keys[pygame.K_q]:
            running = False
        continue

# 終了
pygame.quit()
sys.exit()
