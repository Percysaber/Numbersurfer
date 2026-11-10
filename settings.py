# settings.py - ค่าคงที่ที่ทุกไฟล์ใช้ร่วมกัน
# ถ้าจะแก้ค่าในไฟล์นี้ ต้องแจ้งกลุ่มก่อน

# ---------- หน้าต่าง ----------
WIDTH = 600
HEIGHT = 800
FPS = 60
TITLE = 'Number Surfer'

# ---------- เลน ----------
LANES = 3
LANE_W = WIDTH // LANES          # ความกว้างของแต่ละเลน
PLAYER_Y = HEIGHT - 130          # ตำแหน่ง Y (กึ่งกลาง) ของผู้เล่น


def lane_center_x(lane):
    """คืนค่าพิกัด x กึ่งกลางของเลน (lane = 0, 1, 2)"""
    return lane * LANE_W + LANE_W // 2


# ---------- ความเร็ว (พิกเซลต่อวินาที) ----------
START_SPEED = 220
SPEED_STEP = 12                  # ตอบถูกแล้วเร็วขึ้นเท่านี้
MAX_SPEED = 520
FIRST_QUESTION_DELAY = 1.2       # วินาทีก่อนโจทย์แรกขึ้น
NEXT_QUESTION_DELAY = 0.8        # วินาทีระหว่างโจทย์
PIXELS_PER_METER = 20            # ใช้แปลงระยะที่วิ่งเป็นเมตร

# ---------- คะแนนและหัวใจ ----------
MAX_HEARTS = 3
BASE_POINTS = 10
COMBO_BONUS = 0.1                # คอมโบเพิ่มคะแนน 10% ต่อครั้ง
HEAL_STREAK = 3                  # ตอบถูกติดกันกี่ครั้งถึงได้หัวใจคืน
HIGH_SCORE_FILE = 'highscore.json'

# ---------- ระดับความยาก (ชื่อต้องสะกดตรงกันทุกไฟล์) ----------
EASY = 'Easy'
MEDIUM = 'Medium'
HARD = 'Hard'
LEVELS = [EASY, MEDIUM, HARD]
SCORE_MULTIPLIER = {EASY: 1.0, MEDIUM: 1.5, HARD: 2.0}

# ---------- สี (R, G, B) ----------
BG_COLOR = (30, 30, 46)
ROAD_EDGE_COLOR = (50, 50, 75)
LANE_LINE_COLOR = (90, 90, 125)
WHITE = (240, 240, 240)
GREY = (110, 110, 130)
YELLOW = (250, 210, 80)
RED = (230, 70, 70)
GREEN = (80, 200, 120)
BLUE = (80, 150, 250)
SKIN = (245, 200, 160)
GATE_COLOR = (110, 90, 200)
PANEL_COLOR = (20, 20, 30)
