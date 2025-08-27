# make_assets.py
import pygame, os

W, H = 480, 640
os.makedirs("assets", exist_ok=True)

pygame.init()

def save_png(surface, path):
    pygame.image.save(surface, path)
    print("saved:", path)

# --- player.png（白い丸アイコン） ---
player = pygame.Surface((64, 64), pygame.SRCALPHA)
pygame.draw.circle(player, (255, 255, 255), (32, 32), 28)   # 白丸
pygame.draw.circle(player, (200, 200, 200), (32, 32), 28, 3)  # 縁取り
save_png(player, "assets/player.png")

# --- enemy.png（赤い四角に白い✕） ---
enemy = pygame.Surface((64, 64), pygame.SRCALPHA)
enemy.fill((220, 60, 60))
pygame.draw.line(enemy, (255, 255, 255), (10, 10), (54, 54), 6)
pygame.draw.line(enemy, (255, 255, 255), (54, 10), (10, 54), 6)
save_png(enemy, "assets/enemy.png")

# --- bg.png（簡易グラデ背景） ---
bg = pygame.Surface((W, H))
for y in range(H):
    c = 10 + int(30 * y / H)  # うっすらグラデ
    bg.fill((c, c, c), rect=pygame.Rect(0, y, W, 1))
save_png(bg, "assets/bg.png")

pygame.quit()
