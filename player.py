# player.py - ตัวละครผู้เล่น เปลี่ยนเลนซ้าย/ขวา พร้อมแอนิเมชันวิ่ง
import pygame

from settings import LANES, PLAYER_Y, BLUE, SKIN, YELLOW, WHITE, lane_center_x

PLAYER_W, PLAYER_H = 56, 84
SLIDE_SPEED = 15                 # ยิ่งมาก ยิ่งเลื่อนไปเลนใหม่เร็ว
FRAME_TIME = 0.15                # วินาทีต่อหนึ่งเฟรมของแอนิเมชันวิ่ง


def make_runner_image(step):
    """วาดตัวละครบนกระดานโต้คลื่น step = 0 หรือ 1 (ท่าขาสลับกัน)"""
    image = pygame.Surface((PLAYER_W, PLAYER_H), pygame.SRCALPHA)
    cx = PLAYER_W // 2
    swing = 7 if step == 0 else -7

    pygame.draw.rect(image, YELLOW, (4, PLAYER_H - 12, PLAYER_W - 8, 10), border_radius=5)  # กระดาน
    pygame.draw.line(image, BLUE, (cx - 5, 52), (cx - 5 + swing, PLAYER_H - 13), 6)       # ขาซ้าย
    pygame.draw.line(image, BLUE, (cx + 5, 52), (cx + 5 - swing, PLAYER_H - 13), 6)       # ขาขวา
    pygame.draw.rect(image, BLUE, (cx - 12, 24, 24, 32), border_radius=8)                 # ลำตัว
    pygame.draw.line(image, SKIN, (cx - 12, 30), (cx - 20, 44 - swing), 5)                # แขนซ้าย
    pygame.draw.line(image, SKIN, (cx + 12, 30), (cx + 20, 44 + swing), 5)                # แขนขวา
    pygame.draw.circle(image, SKIN, (cx, 14), 11)                                         # หัว
    pygame.draw.circle(image, WHITE, (cx, 14), 11, 2)
    return image


class Player(pygame.sprite.Sprite):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.lane = 1                                   # เริ่มที่เลนกลาง
        self.frames = [make_runner_image(0), make_runner_image(1)]
        self.frame_index = 0
        self.frame_timer = 0.0
        self.image = self.frames[0]

        self.x = float(lane_center_x(self.lane))
        self.rect = self.image.get_rect(center=(round(self.x), PLAYER_Y))
        self.blink_time = 0.0                          # เวลาที่เหลือของการกระพริบ

    def blink(self, duration):
        """ให้ตัวละครกระพริบ (ใช้ตอนตอบผิด)"""
        self.blink_time = duration

    def move_left(self):
        """คืนค่า True ถ้าย้ายเลนได้จริง (ไม่ได้ชนขอบ)"""
        if self.lane > 0:
            self.lane -= 1
            return True
        return False

    def move_right(self):
        if self.lane < LANES - 1:
            self.lane += 1
            return True
        return False

    def update(self, dt):
        # เลื่อนเข้าหาเลนเป้าหมายทีละนิด (ได้การเคลื่อนที่แบบนุ่มนวล)
        target = lane_center_x(self.lane)
        self.x += (target - self.x) * min(1, SLIDE_SPEED * dt)
        self.rect.centerx = round(self.x)

        # สลับภาพทุก FRAME_TIME วินาที ให้ดูเหมือนวิ่ง
        self.frame_timer += dt
        if self.frame_timer >= FRAME_TIME:
            self.frame_timer -= FRAME_TIME
            self.frame_index = 1 - self.frame_index
            self.image = self.frames[self.frame_index]

        if self.blink_time > 0:
            self.blink_time -= dt

    def draw(self):
        # ระหว่างกระพริบ: ซ่อนตัวละครสลับกับแสดง ทุก 1/12 วินาที
        if self.blink_time > 0 and int(self.blink_time * 12) % 2 == 0:
            return
        self.window.blit(self.image, self.rect)
