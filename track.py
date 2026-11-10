# track.py - พื้นทางวิ่ง 3 เลน เส้นประเลื่อนลงมาให้ดูเหมือนกำลังวิ่ง
import pygame

from settings import (WIDTH, HEIGHT, LANES, LANE_W, BG_COLOR,
                      ROAD_EDGE_COLOR, LANE_LINE_COLOR)

DASH = 40                         # ความยาวเส้นประ
GAP = 40                          # ช่องว่างระหว่างเส้นประ


class Track:

    def __init__(self, window):
        self.window = window
        self.offset = 0.0

    def update(self, dy):
        # เลื่อนเส้นประลง dy พิกเซล ใช้ % ให้วนกลับ ตัวเลขจะไม่โตไม่สิ้นสุด
        self.offset = (self.offset + dy) % (DASH + GAP)

    def draw(self):
        self.window.fill(BG_COLOR)
        pygame.draw.rect(self.window, ROAD_EDGE_COLOR, (0, 0, 6, HEIGHT))
        pygame.draw.rect(self.window, ROAD_EDGE_COLOR, (WIDTH - 6, 0, 6, HEIGHT))
        for i in range(1, LANES):
            x = i * LANE_W
            y = self.offset - (DASH + GAP)
            while y < HEIGHT:
                pygame.draw.line(self.window, LANE_LINE_COLOR, (x, y), (x, y + DASH), 4)
                y += DASH + GAP
