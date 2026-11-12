# question_generator.py - สุ่มโจทย์คณิตศาสตร์ตามระดับ และสุ่มคำตอบหลอก
# คลาสนี้ไม่ใช้ pygame เลย จึงทดสอบด้วย print() ได้ทันที
import random

from settings import EASY, MEDIUM, HARD, LANES


class QuestionGenerator:

    def generate(self, level):
        """คืนค่า (ข้อความโจทย์, คำตอบ, ตัวเลือก 3 ตัวเรียงตามเลน 0-2)"""
        if level == EASY:
            text, answer = self._easy()
        elif level == MEDIUM:
            text, answer = self._medium()
        else:
            text, answer = self._hard()
        choices = self._make_choices(answer)
        return text, answer, choices

    # ---------- ระดับง่าย: บวกลบ 1-2 หลัก ----------
    def _easy(self):
        a = random.randint(1, 99)
        b = random.randint(1, 99)
        op = random.choice(['+', '-'])
        return self._add_or_subtract(a, b, op)

    # ---------- ระดับกลาง: บวกลบคูณ 2 หลัก ----------
    def _medium(self):
        op = random.choice(['+', '-', 'x'])
        if op == 'x':
            a = random.randint(10, 99)
            b = random.randint(2, 9)       # 2 หลัก x 1 หลัก ให้คิดทันขณะวิ่ง
            return f'{a} x {b}', a * b
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        return self._add_or_subtract(a, b, op)

    # ---------- ระดับยาก: (a +- b) */ c มีวงเล็บ ----------
    def _hard(self):
        inner_op = random.choice(['+', '-'])
        outer_op = random.choice(['x', '/'])

        if outer_op == 'x':
            a = random.randint(2, 30)
            b = random.randint(2, 30)
            if inner_op == '-' and b > a:
                a, b = b, a                       # ไม่ให้ในวงเล็บติดลบ
            inner = a + b if inner_op == '+' else a - b
            c = random.randint(2, 9)
            return f'({a} {inner_op} {b}) x {c}', inner * c

        # หารลงตัวเสมอ: สุ่ม "ผลหาร" กับ "ตัวหาร" ก่อน แล้วคูณกลับเป็นตัวตั้ง
        c = random.randint(2, 9)                  # ตัวหาร
        quotient = random.randint(2, 12)          # คำตอบ
        inner = c * quotient                      # ค่าในวงเล็บที่ต้องได้
        if inner_op == '+':
            b = random.randint(1, inner - 1)
            a = inner - b
        else:
            b = random.randint(1, 20)
            a = inner + b
        return f'({a} {inner_op} {b}) / {c}', quotient

    def _add_or_subtract(self, a, b, op):
        if op == '+':
            return f'{a} + {b}', a + b
        if b > a:
            a, b = b, a                           # สลับค่า เพื่อไม่ให้ผลลัพธ์ติดลบ
        return f'{a} - {b}', a - b

    # ---------- คำตอบหลอก ----------
    def _make_choices(self, answer):
        """สุ่มคำตอบหลอกที่ใกล้คำตอบจริง ไม่ซ้ำกัน ไม่ติดลบ แล้วสลับตำแหน่ง"""
        spread = max(3, answer // 5)              # คำตอบยิ่งมาก ยิ่งหลอกได้กว้าง
        wrong = set()                             # ใช้ set กันตัวเลขซ้ำ
        while len(wrong) < LANES - 1:
            fake = answer + random.choice([-1, 1]) * random.randint(1, spread)
            if fake != answer and fake >= 0:
                wrong.add(fake)
        choices = [answer] + list(wrong)
        random.shuffle(choices)                   # คำตอบที่ถูกจะอยู่เลนไหนก็ได้
        return choices


if __name__ == '__main__':
    # รันไฟล์นี้ตรง ๆ เพื่อทดสอบ: python question_generator.py
    qg = QuestionGenerator()
    for level in [EASY, MEDIUM, HARD]:
        print('---', level, '---')
        for _ in range(5):
            text, answer, choices = qg.generate(level)
            print(f'{text} = {answer}   choices={choices}')
