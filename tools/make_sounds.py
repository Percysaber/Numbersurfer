# tools/make_sounds.py - สร้างไฟล์เสียงทั้งหมดของเกมด้วยโค้ด (ไม่มีปัญหาลิขสิทธิ์)
# รันจากโฟลเดอร์หลักของโปรเจกต์:  python tools/make_sounds.py
# จะได้ไฟล์ .wav ในโฟลเดอร์ sounds/
import math
import os
import struct
import wave

RATE = 22050                       # จำนวน sample ต่อวินาที
OUT_DIR = 'sounds'


def tone(freq, duration, volume=0.4, shape='square'):
    """สร้างเสียงหนึ่งโน้ต คืนค่าเป็น list ของ sample (-1 ถึง 1)"""
    n = int(RATE * duration)
    samples = []
    for i in range(n):
        t = i / RATE
        phase = (freq * t) % 1.0
        if freq == 0:
            s = 0.0                                   # โน้ตเงียบ (rest)
        elif shape == 'square':
            s = 1.0 if phase < 0.5 else -1.0
        elif shape == 'triangle':
            s = 4 * abs(phase - 0.5) - 1
        else:                                         # sine
            s = math.sin(2 * math.pi * phase)
        # envelope: ค่อย ๆ ดังขึ้นตอนต้น และค่อย ๆ เบาลงตอนท้าย กันเสียงคลิก
        attack = min(1.0, i / (RATE * 0.005))
        release = min(1.0, (n - i) / (RATE * 0.03))
        samples.append(s * volume * attack * release)
    return samples


def mix(*tracks):
    """รวมหลาย track ให้เล่นพร้อมกัน"""
    length = max(len(t) for t in tracks)
    out = [0.0] * length
    for track in tracks:
        for i, s in enumerate(track):
            out[i] += s
    return out


def save(name, samples):
    path = os.path.join(OUT_DIR, name)
    with wave.open(path, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)                             # 16-bit
        f.setframerate(RATE)
        data = b''.join(struct.pack('<h', int(max(-1, min(1, s)) * 32767))
                        for s in samples)
        f.writeframes(data)
    print('saved', path)


def note(name):
    """แปลงชื่อโน้ต เช่น 'A4' เป็นความถี่ (Hz)"""
    names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    index = names.index(name[:-1]) + 12 * (int(name[-1]) + 1)
    return 440 * 2 ** ((index - 69) / 12)


def make_effects():
    save('correct.wav', tone(note('E5'), 0.08, 0.3) + tone(note('B5'), 0.18, 0.3))
    save('wrong.wav', tone(220, 0.12, 0.35) + tone(150, 0.3, 0.35))
    save('move.wav', tone(700, 0.04, 0.25, 'sine'))
    save('heart.wav', tone(note('C6'), 0.07, 0.25, 'triangle') +
         tone(note('E6'), 0.07, 0.25, 'triangle') + tone(note('G6'), 0.15, 0.25, 'triangle'))
    save('gameover.wav', sum((tone(note(n), 0.22, 0.3, 'triangle')
                              for n in ['C5', 'G4', 'E4', 'C4']), []))


def make_music():
    """เพลงพื้นหลัง 8 ห้อง วนซ้ำได้: คอร์ด Am - F - C - G"""
    eighth = 60 / 140 / 2                             # ความยาวโน้ตเขบ็ต 1 ชั้น ที่ 140 BPM
    chords = [['A4', 'C5', 'E5'], ['F4', 'A4', 'C5'],
              ['C5', 'E5', 'G5'], ['G4', 'B4', 'D5']]
    basses = ['A2', 'F2', 'C3', 'G2']
    pattern = [0, 1, 2, 1, 0, 2, 1, 2]               # ลำดับการเล่นโน้ตในคอร์ด (arpeggio)

    melody, bass = [], []
    for repeat in range(2):
        for chord, root in zip(chords, basses):
            for step in pattern:
                melody += tone(note(chord[step]), eighth, 0.12, 'square')
            for _ in range(4):
                bass += tone(note(root), eighth * 2, 0.22, 'triangle')
    save('music.wav', mix(melody, bass))


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    make_effects()
    make_music()
