# particle_test.py — Pyxel によるパーティクルデモ
#
# Original code: “particle test” by Time_Tripper (PICO-8)
# https://www.lexaloffle.com/bbs/?tid=27751
#
# This work is based on the above original under CC BY-NC-SA 4.0.
# https://creativecommons.org/licenses/by-nc-sa/4.0/
#
# This Pyxel version is an adaptation / translation into Python.
# Licensed under CC BY-NC-SA 4.0.
#
# このプログラムは上記 PICO-8 用コードを参考にして、
# Python + Pyxel 向けに移植・改変したものです。
#
# 変更点:
# - PICO-8 から Pyxel への移植に伴い、キー操作や描画処理を変更
# - 寿命が尽きた粒子は新しい粒子に置き換えるように改変
# - Pyxel の API に合わせてコードを調整

# particle_test.py
import pyxel
import random
import math

W, H = 128, 128


class Bit:
    def __init__(self):
        self.f = random.uniform(0, 100)
        self.x = random.uniform(0, W)
        self.y = random.uniform(0, H)
        self.c = random.randint(1, 15)
        self.dx = 3 - random.uniform(0, 6)
        self.dy = 3 - random.uniform(0, 6)

    def move(self, target_x, target_y):
        if self.f < 0:
            return False  # 消去対象
        self.x += self.dx
        self.y += self.dy
        self.dx += (target_x - self.x) / 100
        self.dy += (target_y - self.y) / 100
        self.f -= 1
        self.dx *= 0.99
        self.dy *= 0.99

        # 画面端で反射
        if self.x < 0 or self.x > W - 1:
            self.dx *= -1
        if self.y < 0 or self.y > H - 1:
            self.dy *= -1

        return True

    def draw(self):
        pyxel.line(
            int(self.x),
            int(self.y),
            int(self.x + self.dx),
            int(self.y + self.dy),
            self.c,
        )


class App:
    def __init__(self):
        pyxel.init(W, H, title="Particle Test")
        self.x = W // 2
        self.y = H // 2
        self.bits = [Bit() for _ in range(500)]
        # pyxel.load("")  # 効果音読み込みをする場合ここにファイルパス
        pyxel.run(self.update, self.draw)

    def make_bit(self):
        self.bits.append(Bit())

    def del_bit(self):
        if self.bits:
            self.bits.pop(0)

    def update(self):
        # 移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 3
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 3
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 3
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 3

        # 追加・削除（Z/Xキーなどに割り当て）
        if pyxel.btnp(pyxel.KEY_Z):
            # pyxel.play(0, 0)  # 効果音再生
            self.make_bit()
        if pyxel.btnp(pyxel.KEY_X):
            # pyxel.play(0, 2)
            self.del_bit()

        # パーティクル更新
        new_bits = []
        for b in self.bits:
            if b.move(self.x, self.y):
                new_bits.append(b)
            else:
                # 消えたビットは新しく生成
                new_bits.append(Bit())
        self.bits = new_bits

    def draw(self):
        pyxel.cls(0)
        for b in self.bits:
            b.draw()
        # pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, 0)  # スプライト描画したい場合
        pyxel.text(0, 0, f"count={len(self.bits)}", 12)


App()
