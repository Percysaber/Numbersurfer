# effects.py - เอฟเฟกต์ภาพทั้งหมดของเกม
#   FloatingText : ข้อความลอยขึ้นแล้วจาง เช่น "+15", "Heart +1"
#   GateFlash    : ประตูที่วิ่งผ่าน ขยายตัวแล้วจางหายเป็นสีเขียว (ถูก) หรือแดง (ผิด)
#   Particle     : เศษประกายหนึ่งชิ้น ใช้หลายชิ้นรวมกันเป็นการระเบิด
# ทุกคลาสเป็น Sprite: Game เก็บไว้ใน Group เดียว แล้วเรียก update(dt) / draw() ทุกเฟรม
# เมื่อหมดเวลา แต่ละชิ้นเรียก self.kill() เพื่อลบตัวเองออกจาก Group
import math
import random

import pygame

GREEN_SPARKS = [(80, 200, 120), (140, 240, 160), (250, 210, 80), (255, 255, 255)]
RED_SHARDS = [(230, 70, 70), (180, 40, 40), (255, 120, 120)]


class FloatingText(pygame.sprite.Sprite):

    DURATION = 0.9                # วินาทีที่ข้อความแสดงอยู่
    RISE_SPEED = 70               # พิกเซลต่อวินาทีที่ลอยขึ้น

    def __init__(self, window, text, color, center, size=40):
        super().__init__()
        self.window = window
        font = pygame.font.Font(None, size)
        self.base_image = font.render(text, True, color)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=center)
        self.y = float(self.rect.y)
        self.life = FloatingText.DURATION

    def update(self, dt):
        self.life -= dt
        if self.life <= 0:
            self.kill()
            return
        self.y -= FloatingText.RISE_SPEED * dt
        self.rect.y = round(self.y)
        self.image = self.base_image.copy()
        self.image.set_alpha(int(255 * self.life / FloatingText.DURATION))

    def draw(self):
        self.window.blit(self.image, self.rect)


class GateFlash(pygame.sprite.Sprite):
    """ภาพประตูที่ถูกย้อมสี แล้วขยายใหญ่ขึ้นพร้อมจางหาย"""

    DURATION = 0.4
    GROW = 0.5                    # ขยายใหญ่สุด 1.5 เท่าของขนาดเดิม

    def __init__(self, window, gate_image, center, color):
        super().__init__()
        self.window = window
        self.center = center
        # ย้อมสีประตู: วางสี่เหลี่ยมสีโปร่งแสงทับภาพประตูเดิม
        self.base_image = gate_image.copy()
        tint = pygame.Surface(self.base_image.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(tint, (*color, 210), tint.get_rect(), border_radius=12)
        self.base_image.blit(tint, (0, 0))
        self.image = self.base_image
        self.rect = self.image.get_rect(center=center)
        self.life = GateFlash.DURATION

    def update(self, dt):
        self.life -= dt
        if self.life <= 0:
            self.kill()
            return
        progress = 1 - self.life / GateFlash.DURATION          # 0 -> 1
        scale = 1 + GateFlash.GROW * progress
        w, h = self.base_image.get_size()
        self.image = pygame.transform.smoothscale(self.base_image,
                                                  (int(w * scale), int(h * scale)))
        self.image.set_alpha(int(255 * (1 - progress)))
        self.rect = self.image.get_rect(center=self.center)

    def draw(self):
        self.window.blit(self.image, self.rect)


class Particle(pygame.sprite.Sprite):
    """ประกายหนึ่งชิ้น: พุ่งออกไปในทิศสุ่ม ตกลงตามแรงโน้มถ่วง และเล็กลงเรื่อย ๆ"""

    GRAVITY = 600                 # พิกเซลต่อวินาทีกำลังสอง

    def __init__(self, window, center, color, speed, size, life):
        super().__init__()
        self.window = window
        self.x, self.y = center
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - speed * 0.5   # เอียงขึ้นด้านบนเล็กน้อย
        self.color = color
        self.size = size
        self.life = self.max_life = life

    def update(self, dt):
        self.life -= dt
        if self.life <= 0:
            self.kill()
            return
        self.vy += Particle.GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self):
        radius = max(1, round(self.size * self.life / self.max_life))
        pygame.draw.circle(self.window, self.color, (round(self.x), round(self.y)), radius)


def burst(window, center, colors, count, speed, size, life):
    """สร้างประกายหลายชิ้นพร้อมกัน คืนค่าเป็น list เพื่อเอาไปใส่ใน Group"""
    return [Particle(window, center, random.choice(colors),
                     random.uniform(speed * 0.4, speed), size, random.uniform(life * 0.6, life))
            for _ in range(count)]


def correct_effect(window, gate):
    """ผ่านประตูถูก: ประตูเรืองเขียวขยายตัว + ประกายสีเขียว/ทองพุ่งรอบทิศ"""
    effects = [GateFlash(window, gate.image, gate.rect.center, (80, 200, 120))]
    effects += burst(window, gate.rect.center, GREEN_SPARKS, count=30,
                     speed=380, size=6, life=0.7)
    return effects


def wrong_effect(window, wrong_gate, correct_gate):
    """ผ่านประตูผิด: ประตูแตกเป็นเศษสีแดง + ประตูที่ถูกเรืองเขียว ให้รู้ว่าควรไปเลนไหน"""
    effects = [GateFlash(window, wrong_gate.image, wrong_gate.rect.center, (230, 70, 70))]
    effects += burst(window, wrong_gate.rect.center, RED_SHARDS, count=20,
                     speed=300, size=8, life=0.6)
    effects.append(GateFlash(window, correct_gate.image, correct_gate.rect.center,
                             (80, 200, 120)))
    return effects
