# main.py - จุดเริ่มเกม ตาม 12-step template ใน lecture
# รันด้วย: python main.py  (ต้องรันจากโฟลเดอร์นี้ เพื่อให้หาโฟลเดอร์ sounds/ เจอ)

# 1 - Import packages
import os
import sys

import pygame

from settings import WIDTH, HEIGHT, FPS, TITLE
from game import Game

# ให้ path ของไฟล์เสียงและ highscore.json อ้างจากโฟลเดอร์ของเกมเสมอ
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 2 - Define constants  (อยู่ใน settings.py)
MAX_DT = 0.05                     # กันเกมกระโดดไกล ถ้าเฟรมค้าง (เช่น ตอนลากหน้าต่าง)

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# 4 - Load assets  (แต่ละคลาสโหลดของตัวเองตอนสร้าง)

# 5 - Initialize variables
game = Game(window)

# 6 - Loop forever
while True:

    # 7 - Check for and handle events: main อ่าน event แล้วส่งต่อให้ Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.handle_event(event)

    # 8 - Do any "per frame" actions
    dt = min(clock.get_time() / 1000, MAX_DT)   # วินาทีที่ผ่านไปจากเฟรมก่อน
    game.update(dt)

    # 9 - Clear the window  /  10 - Draw all window elements
    game.draw()

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FPS)
