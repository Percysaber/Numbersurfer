# high_score.py - บันทึกคะแนนสูงสุดของแต่ละระดับลงไฟล์ JSON
import json
import os

from settings import LEVELS, HIGH_SCORE_FILE


class HighScore:

    def __init__(self, path=HIGH_SCORE_FILE):
        self.path = path
        self.best = {level: 0 for level in LEVELS}
        self._load()

    def get(self, level):
        return self.best[level]

    def submit(self, level, score):
        """ส่งคะแนนเมื่อจบเกม คืนค่า True ถ้าทำสถิติใหม่"""
        if score > self.best[level]:
            self.best[level] = score
            self._save()
            return True
        return False

    def _load(self):
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, encoding='utf-8') as f:
                data = json.load(f)
            for level in LEVELS:
                self.best[level] = int(data.get(level, 0))
        except (ValueError, OSError):
            pass                                      # ไฟล์เสีย: เริ่มนับใหม่

    def _save(self):
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.best, f, indent=2)
        except OSError:
            pass                                      # เขียนไฟล์ไม่ได้ ก็เล่นต่อได้
