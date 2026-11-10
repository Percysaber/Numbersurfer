# sound_manager.py - ดนตรีพื้นหลังและเสียงประกอบ
# ไฟล์เสียงสร้างด้วย tools/make_sounds.py และอยู่ในโฟลเดอร์ sounds/
# ถ้าไม่มีไฟล์หรือเครื่องไม่มีการ์ดเสียง เกมจะเล่นต่อได้แบบไม่มีเสียง
import os

import pygame

SOUND_DIR = 'sounds'
MUSIC_FILE = os.path.join(SOUND_DIR, 'music.wav')

# ความดังของเสียง 0.0 (เงียบ) ถึง 1.0 (ดังสุด) ปรับตรงนี้ที่เดียว
MUSIC_VOLUME = 0.15
EFFECT_VOLUMES = {
    'correct': 0.3,
    'wrong': 0.3,
    'move': 0.12,
    'heart': 0.3,
    'gameover': 0.35,
}


class SoundManager:

    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False
        # โหลดเสียงครั้งเดียวตอนเริ่ม ไม่โหลดใหม่ทุกครั้งที่เล่น
        self.sounds = {}
        for name, volume in EFFECT_VOLUMES.items():
            self.sounds[name] = self._load(os.path.join(SOUND_DIR, name + '.wav'), volume)

    def _load(self, path, volume):
        if self.enabled and os.path.exists(path):
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        return None

    def _play(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    # ---------- เพลงพื้นหลัง ----------
    def play_music(self):
        if self.enabled and os.path.exists(MUSIC_FILE):
            pygame.mixer.music.load(MUSIC_FILE)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)                # -1 = เล่นวนไม่รู้จบ

    def pause_music(self):
        if self.enabled:
            pygame.mixer.music.pause()

    def resume_music(self):
        if self.enabled:
            pygame.mixer.music.unpause()

    # ---------- เสียงประกอบ ----------
    def play_correct(self):
        self._play('correct')

    def play_wrong(self):
        self._play('wrong')

    def play_move(self):
        self._play('move')

    def play_heart(self):
        self._play('heart')

    def play_game_over(self):
        self._play('gameover')
