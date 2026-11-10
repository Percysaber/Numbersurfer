# score_manager.py - คะแนน คอมโบ และหัวใจ
from settings import (SCORE_MULTIPLIER, MAX_HEARTS, BASE_POINTS,
                      COMBO_BONUS, HEAL_STREAK)


class ScoreManager:

    def __init__(self, level):
        self.multiplier = SCORE_MULTIPLIER[level]
        self.score = 0
        self.combo = 0            # ตอบถูกติดกันกี่ครั้ง (ใช้คิดโบนัส)
        self.streak = 0           # นับไปถึง HEAL_STREAK เพื่อคืนหัวใจ แล้วเริ่มนับใหม่
        self.hearts = MAX_HEARTS

    def on_correct(self):
        """เรียกเมื่อตอบถูก คืนค่าคะแนนที่ได้รอบนี้"""
        self.combo += 1
        self.streak += 1
        bonus = 1 + COMBO_BONUS * (self.combo - 1)
        points = int(BASE_POINTS * self.multiplier * bonus)
        self.score += points

        if self.streak == HEAL_STREAK:
            self.streak = 0
            if self.hearts < MAX_HEARTS:
                self.hearts += 1
        return points

    def on_wrong(self):
        """เรียกเมื่อตอบผิด: เสียหัวใจ 1 ดวง และคอมโบกลับเป็น 0"""
        self.hearts -= 1
        self.combo = 0
        self.streak = 0

    def is_game_over(self):
        return self.hearts <= 0
