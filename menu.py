# menu.py - หน้าเมนูเลือกระดับความยาก พร้อมคะแนนสูงสุดและแอนิเมชัน
#   Button      : ปุ่มแบบ SimpleButton ใน lecture (handle_event() คืน True เมื่อถูกคลิก)
#                 ขยายขึ้นนิด ๆ เมื่อเอาเมาส์ชี้
#   MenuSymbol  : ตัวเลข/เครื่องหมายคณิตศาสตร์ที่ลอยขึ้นด้านหลัง
#   MenuScreen  : รวมทุกอย่าง + พื้นทางวิ่งเลื่อน + ตัวละครวิ่งสลับเลน
import math
import random

import pygame

from settings import (WIDTH, HEIGHT, LANES, EASY, MEDIUM, HARD, SCORE_MULTIPLIER,
                      WHITE, GREY, YELLOW, GATE_COLOR, PANEL_COLOR, lane_center_x)
from track import Track
from player import make_runner_image

MENU_SCROLL_SPEED = 160          # ความเร็วพื้นทางวิ่งในหน้าเมนู (พิกเซล/วินาที)
SYMBOL_COUNT = 18                # จำนวนตัวเลข/เครื่องหมายที่ลอยอยู่
RUNNER_Y = 665                   # ตำแหน่ง Y ของตัวละครในหน้าเมนู
RUNNER_SWITCH_TIME = 1.3         # ตัวละครเปลี่ยนเลนทุกกี่วินาที


class Button:

    def __init__(self, window, center, text):
        self.window = window
        self.rect = pygame.Rect(0, 0, 320, 64)
        self.rect.center = center
        self.text = text
        self.font = pygame.font.Font(None, 44)
        self.pressed = False
        self.hover_amount = 0.0                       # 0 = ปกติ, 1 = ขยายเต็มที่

    def handle_event(self, event):
        """คืนค่า True เมื่อกดและปล่อยเมาส์บนปุ่ม (คลิกครบ 1 ครั้ง)"""
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            clicked = self.pressed and self.rect.collidepoint(event.pos)
            self.pressed = False
            return clicked
        return False

    def update(self, dt):
        # ค่อย ๆ ขยายเมื่อเมาส์ชี้ และค่อย ๆ หดกลับเมื่อเมาส์ออก
        target = 1.0 if self.rect.collidepoint(pygame.mouse.get_pos()) else 0.0
        self.hover_amount += (target - self.hover_amount) * min(1, 12 * dt)

    def draw(self):
        grow = round(12 * self.hover_amount)
        box = self.rect.inflate(grow * 2, grow)
        color = GATE_COLOR if self.hover_amount > 0.5 else PANEL_COLOR
        pygame.draw.rect(self.window, color, box, border_radius=12)
        pygame.draw.rect(self.window, GATE_COLOR, box, 2, border_radius=12)
        label = self.font.render(self.text, True, WHITE)
        self.window.blit(label, label.get_rect(center=box.center))


class MenuSymbol:
    """ตัวเลขหรือเครื่องหมายหนึ่งตัวที่ลอยขึ้นช้า ๆ แกว่งซ้ายขวา แล้ววนกลับไปด้านล่าง"""

    CHARACTERS = '0123456789+-x/=?'

    def __init__(self, start_anywhere):
        self.reset()
        if start_anywhere:
            self.y = random.uniform(0, HEIGHT)        # ตอนเปิดเมนูให้กระจายเต็มจอ

    def reset(self):
        size = random.randint(28, 64)
        font = pygame.font.Font(None, size)
        self.image = font.render(random.choice(MenuSymbol.CHARACTERS), True, GATE_COLOR)
        self.image.set_alpha(random.randint(50, 120))  # โปร่งแสง ไม่แย่งความสนใจ
        self.base_x = random.uniform(20, WIDTH - 20)
        self.y = HEIGHT + 40
        self.speed = random.uniform(25, 70)
        self.wave = random.uniform(0, 2 * math.pi)     # จุดเริ่มของการแกว่ง

    def update(self, dt):
        self.y -= self.speed * dt
        self.wave += dt
        if self.y < -40:
            self.reset()

    def draw(self, window):
        x = self.base_x + math.sin(self.wave) * 15
        window.blit(self.image, self.image.get_rect(center=(round(x), round(self.y))))


class MenuScreen:

    KEYS = {pygame.K_1: EASY, pygame.K_2: MEDIUM, pygame.K_3: HARD}

    def __init__(self, window, high_scores):
        self.window = window
        self.high_scores = high_scores
        self.font_title = pygame.font.Font(None, 80)
        self.font_small = pygame.font.Font(None, 30)
        self.font_tiny = pygame.font.Font(None, 24)
        cx = WIDTH // 2
        self.buttons = {}
        for i, level in enumerate([EASY, MEDIUM, HARD]):
            text = f'{i + 1}. {level}  (x{SCORE_MULTIPLIER[level]})'
            self.buttons[level] = Button(window, (cx, 360 + i * 100), text)

        # แอนิเมชันพื้นหลัง
        self.track = Track(window)
        self.symbols = [MenuSymbol(start_anywhere=True) for _ in range(SYMBOL_COUNT)]
        self.runner_frames = [make_runner_image(0), make_runner_image(1)]
        self.runner_lane = 1
        self.runner_x = float(lane_center_x(1))
        self.switch_timer = RUNNER_SWITCH_TIME
        self.time = 0.0                               # เวลารวม ใช้กับการขยับขึ้นลงของชื่อเกม

    def handle_event(self, event):
        """คืนค่าระดับที่เลือก ('Easy', 'Medium', 'Hard') หรือ None"""
        if event.type == pygame.KEYDOWN and event.key in self.KEYS:
            return self.KEYS[event.key]
        for level, button in self.buttons.items():
            if button.handle_event(event):
                return level
        return None

    def update(self, dt):
        self.time += dt
        self.track.update(MENU_SCROLL_SPEED * dt)
        for symbol in self.symbols:
            symbol.update(dt)
        for button in self.buttons.values():
            button.update(dt)

        # ตัวละครเปลี่ยนไปเลนอื่นแบบสุ่มเป็นระยะ แล้วเลื่อนไปอย่างนุ่มนวล
        self.switch_timer -= dt
        if self.switch_timer <= 0:
            self.switch_timer = RUNNER_SWITCH_TIME
            self.runner_lane = random.choice([lane for lane in range(LANES)
                                              if lane != self.runner_lane])
        target = lane_center_x(self.runner_lane)
        self.runner_x += (target - self.runner_x) * min(1, 6 * dt)

    def draw(self):
        cx = WIDTH // 2
        self.track.draw()
        for symbol in self.symbols:
            symbol.draw(self.window)

        frame = self.runner_frames[int(self.time / 0.15) % 2]   # สลับท่าวิ่งทุก 0.15 วินาที
        self.window.blit(frame, frame.get_rect(center=(round(self.runner_x), RUNNER_Y)))

        title_y = 180 + math.sin(self.time * 2) * 8              # ชื่อเกมขยับขึ้นลง
        self._text('NUMBER SURFER', self.font_title, PANEL_COLOR, (cx + 4, title_y + 4))  # เงา
        self._text('NUMBER SURFER', self.font_title, YELLOW, (cx, title_y))
        self._text('Run into the gate with the right answer!', self.font_small, WHITE, (cx, 255))

        for level, button in self.buttons.items():
            button.draw()
            best = self.high_scores.get(level)
            self._text(f'Best: {best}', self.font_tiny, GREY, (cx, button.rect.bottom + 16))
        self._text('Move: Left/Right or A/D     Pause: P', self.font_small, GREY, (cx, 750))

    def _text(self, text, font, color, center):
        surface = font.render(text, True, color)
        self.window.blit(surface, surface.get_rect(center=(round(center[0]), round(center[1]))))
