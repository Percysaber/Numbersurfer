# gate.py - ประตูคำตอบหนึ่งบาน
import pygame

from settings import LANE_W, GATE_COLOR, WHITE, lane_center_x

GATE_HEIGHT = 70


class Gate(pygame.sprite.Sprite):

    def __init__(self, window, lane, value, is_correct):
        super().__init__()
        self.window = window
        self.lane = lane
        self.value = value
        self.is_correct = is_correct

        # วาดรูปประตูครั้งเดียวตอนสร้าง (ไม่ต้องวาดใหม่ทุกเฟรม)
        width = LANE_W - 30
        self.image = pygame.Surface((width, GATE_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(self.image, GATE_COLOR, self.image.get_rect(), border_radius=12)
        font = pygame.font.Font(None, 52)
        text = font.render(str(value), True, WHITE)
        self.image.blit(text, text.get_rect(center=self.image.get_rect().center))

        self.rect = self.image.get_rect(centerx=lane_center_x(lane), bottom=0)
        self.y = float(self.rect.y)   # เก็บตำแหน่งแบบทศนิยม เพื่อให้เลื่อนลื่น

    def update(self, dy):
        """เลื่อนประตูลงมา dy พิกเซล (Group.update(dy) จะเรียกทุกบาน)"""
        self.y += dy
        self.rect.y = round(self.y)

    def draw(self):
        self.window.blit(self.image, self.rect)
