# game.py - คุมกติกาและสถานะของเกม (เมนู / เล่น / หยุดชั่วคราว / จบเกม)
import random

import pygame

from settings import (BG_COLOR, EASY, START_SPEED, SPEED_STEP, MAX_SPEED,
                      FIRST_QUESTION_DELAY, NEXT_QUESTION_DELAY,
                      PIXELS_PER_METER, WIDTH, HEIGHT, PLAYER_Y, GREEN, RED, YELLOW)
from track import Track
from player import Player
from gate import Gate
from question_generator import QuestionGenerator
from score_manager import ScoreManager
from high_score import HighScore
from effects import FloatingText, correct_effect, wrong_effect
from hud import HUD
from sound_manager import SoundManager
from menu import MenuScreen


SHAKE_TIME = 0.3                 # วินาทีที่จอสั่นตอนตอบผิด
SHAKE_SIZE = 10                  # สั่นแรงสุดกี่พิกเซล


class Game:

    STATE_MENU = 'menu'
    STATE_PLAY = 'play'
    STATE_PAUSE = 'pause'
    STATE_OVER = 'over'

    def __init__(self, window):
        self.window = window
        self.high_scores = HighScore()
        self.menu = MenuScreen(window, self.high_scores)
        self.hud = HUD(window)
        self.sound = SoundManager()
        self.question_generator = QuestionGenerator()
        self.track = Track(window)
        self.state = Game.STATE_MENU
        self.level = EASY
        self.sound.play_music()

    def start(self, level):
        """เริ่มรอบใหม่ (เรียกจากเมนู หรือกด R ตอนจบเกม)"""
        self.level = level
        self.player = Player(self.window)
        self.scores = ScoreManager(level)
        self.gates = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.question = ''
        self.answer = None
        self.speed = START_SPEED
        self.distance = 0.0                    # ระยะที่วิ่ง (เมตร)
        self.wait = FIRST_QUESTION_DELAY       # เวลาที่เหลือก่อนโจทย์ถัดไป
        self.flash = None                      # (สี, เวลาที่เหลือ) กระพริบจอตอนถูก/ผิด
        self.shake = 0.0                       # เวลาที่เหลือของการสั่นจอ
        self.new_record = False
        self.state = Game.STATE_PLAY

    # ---------- รับ event ที่ main ส่งมา ----------
    def handle_event(self, event):
        if self.state == Game.STATE_MENU:
            level = self.menu.handle_event(event)
            if level is not None:
                self.start(level)
            return

        if event.type != pygame.KEYDOWN:
            return

        if self.state == Game.STATE_PLAY:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                if self.player.move_left():
                    self.sound.play_move()
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                if self.player.move_right():
                    self.sound.play_move()
            elif event.key in (pygame.K_p, pygame.K_ESCAPE):
                self.state = Game.STATE_PAUSE
                self.sound.pause_music()

        elif self.state == Game.STATE_PAUSE:
            if event.key in (pygame.K_p, pygame.K_ESCAPE):
                self.state = Game.STATE_PLAY
                self.sound.resume_music()
            elif event.key == pygame.K_m:
                self.sound.resume_music()
                self.state = Game.STATE_MENU

        elif self.state == Game.STATE_OVER:
            if event.key == pygame.K_r:
                self.start(self.level)
            elif event.key == pygame.K_m:
                self.state = Game.STATE_MENU

    # ---------- อัปเดตทุกเฟรม ----------
    def update(self, dt):
        if self.state == Game.STATE_MENU:
            self.menu.update(dt)                # แอนิเมชันหน้าเมนู
            return
        if self.state != Game.STATE_PLAY:
            return

        dy = self.speed * dt                    # ระยะที่ทุกอย่างเลื่อนลงในเฟรมนี้
        self.distance += dy / PIXELS_PER_METER
        self.track.update(dy)
        self.player.update(dt)
        self.effects.update(dt)

        if len(self.gates) == 0:
            self.wait -= dt
            if self.wait <= 0:
                self.spawn_question()

        self.gates.update(dy)                   # เรียก Gate.update(dy) ทุกบาน
        self.check_gate_hit()

        if self.flash:
            color, time_left = self.flash
            time_left -= dt
            self.flash = (color, time_left) if time_left > 0 else None
        if self.shake > 0:
            self.shake -= dt

        if self.scores.is_game_over():
            self.end_game()

    def spawn_question(self):
        text, answer, choices = self.question_generator.generate(self.level)
        self.question = text
        self.answer = answer
        for lane, value in enumerate(choices):
            self.gates.add(Gate(self.window, lane, value, value == answer))

    def check_gate_hit(self):
        """ผู้เล่นชนประตูหรือยัง ถ้าชนแล้ว ดูว่าเป็นประตูในเลนเดียวกับผู้เล่นหรือไม่"""
        hits = pygame.sprite.spritecollide(self.player, self.gates, False)
        if not hits:
            return
        # ระหว่างเลื่อนเลน ตัวละครอาจแตะ 2 บาน จึงตัดสินจากเลนที่ผู้เล่นอยู่
        chosen = next((g for g in self.gates if g.lane == self.player.lane), None)
        if chosen is None:                      
            return
        correct_gate = next(g for g in self.gates if g.is_correct)
        above_player = (self.player.rect.centerx, PLAYER_Y - 150)   # เหนือประตู ไม่ทับกัน

        if chosen.is_correct:
            hearts_before = self.scores.hearts
            points = self.scores.on_correct()
            self.speed = min(self.speed + SPEED_STEP, MAX_SPEED)
            self.sound.play_correct()
            self.effects.add(correct_effect(self.window, chosen))
            self.effects.add(FloatingText(self.window, f'+{points}', GREEN, above_player))
            if self.scores.hearts > hearts_before:
                self.sound.play_heart()
                self.effects.add(FloatingText(self.window, 'Heart +1', RED,
                                              (above_player[0], above_player[1] - 40)))
        else:
            self.scores.on_wrong()
            self.sound.play_wrong()
            self.flash = (RED, 0.25)
            self.shake = SHAKE_TIME
            self.player.blink(0.6)
            self.effects.add(wrong_effect(self.window, chosen, correct_gate))
            self.effects.add(FloatingText(self.window, f'Answer: {self.answer}', YELLOW,
                                          above_player, size=36))

        self.gates.empty()                      # ลบประตูทั้งแถว
        self.question = ''
        self.wait = NEXT_QUESTION_DELAY

    def end_game(self):
        self.state = Game.STATE_OVER
        self.new_record = self.high_scores.submit(self.level, self.scores.score)
        self.sound.play_game_over()

    # ---------- วาดหน้าจอ ----------
    def draw(self):
        if self.state == Game.STATE_MENU:
            self.menu.draw()
            return

        self.track.draw()
        for gate in self.gates:
            gate.draw()
        self.player.draw()
        for effect in self.effects:
            effect.draw()

        # สั่นจอ: เลื่อนภาพทั้งฉากไปตำแหน่งสุ่ม ยิ่งใกล้หมดเวลา ยิ่งสั่นน้อยลง
        # (วาด HUD ทีหลัง ตัวเลขคะแนนจึงไม่สั่นตาม อ่านง่าย)
        if self.shake > 0 and self.state == Game.STATE_PLAY:
            power = round(SHAKE_SIZE * self.shake / SHAKE_TIME)
            offset = (random.randint(-power, power), random.randint(-power, power))
            scene = self.window.copy()
            self.window.fill(BG_COLOR)
            self.window.blit(scene, offset)

        self.hud.draw(self.question, self.scores.score, self.scores.combo,
                      self.scores.hearts, self.level, self.distance)

        if self.flash:
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((*self.flash[0], 35))
            self.window.blit(shade, (0, 0))

        if self.state == Game.STATE_PAUSE:
            self.hud.draw_paused()
        elif self.state == Game.STATE_OVER:
            self.hud.draw_game_over(self.scores.score, self.level, self.distance,
                                    self.high_scores.get(self.level), self.new_record)
