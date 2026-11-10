# hud.py - แสดงป้ายโจทย์ คะแนน คอมโบ ระยะทาง ระดับ หัวใจ และหน้าจอหยุด/จบเกม
import pygame

from settings import (WIDTH, HEIGHT, MAX_HEARTS, WHITE, GREY, YELLOW, RED,
                      GREEN, PANEL_COLOR)


class HUD:

    def __init__(self, window):
        self.window = window
        self.font_big = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

    def draw(self, question, score, combo, hearts, level, distance):
        if question:
            self._draw_question(question)
        self._draw_text(f'Score: {score}', self.font_small, WHITE, topleft=(14, 10))
        combo_color = YELLOW if combo >= 3 else WHITE
        self._draw_text(f'Combo: x{combo}', self.font_small, combo_color, topleft=(14, 40))
        self._draw_text(f'{int(distance)} m', self.font_small, WHITE, midtop=(WIDTH // 2, 10))
        self._draw_text(level, self.font_small, WHITE, topright=(WIDTH - 14, 40))
        for i in range(MAX_HEARTS):
            color = RED if i < hearts else GREY
            self._draw_heart(WIDTH - 28 - i * 34, 20, color)

    def draw_paused(self):
        self._shade(140)
        cx = WIDTH // 2
        self._draw_text('PAUSED', self.font_big, YELLOW, center=(cx, 360))
        self._draw_text('P = resume    M = menu', self.font_small, WHITE, center=(cx, 430))

    def draw_game_over(self, score, level, distance, best, new_record):
        self._shade(180)
        cx = WIDTH // 2
        self._draw_text('GAME OVER', self.font_big, RED, center=(cx, 270))
        self._draw_text(f'Score: {score}', self.font, WHITE, center=(cx, 350))
        self._draw_text(f'Distance: {int(distance)} m   ({level})', self.font_small, WHITE,
                        center=(cx, 400))
        if new_record:
            self._draw_text('NEW RECORD!', self.font, GREEN, center=(cx, 455))
        else:
            self._draw_text(f'Best: {best}', self.font_small, GREY, center=(cx, 455))
        self._draw_text('R = play again    M = menu', self.font_small, WHITE, center=(cx, 530))

    # ---------- ตัวช่วยภายในคลาส ----------
    def _draw_question(self, question):
        box = pygame.Rect(40, 72, WIDTH - 80, 84)
        pygame.draw.rect(self.window, PANEL_COLOR, box, border_radius=14)
        pygame.draw.rect(self.window, YELLOW, box, 3, border_radius=14)
        self._draw_text(f'{question} = ?', self.font_big, YELLOW, center=box.center)

    def _draw_text(self, text, font, color, **position):
        surface = font.render(text, True, color)
        self.window.blit(surface, surface.get_rect(**position))

    def _shade(self, alpha):
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, alpha))
        self.window.blit(shade, (0, 0))

    def _draw_heart(self, cx, cy, color):
        # หัวใจ = วงกลม 2 วง + สามเหลี่ยมด้านล่าง
        pygame.draw.circle(self.window, color, (cx - 6, cy - 3), 7)
        pygame.draw.circle(self.window, color, (cx + 6, cy - 3), 7)
        pygame.draw.polygon(self.window, color, [(cx - 13, cy), (cx + 13, cy), (cx, cy + 14)])
