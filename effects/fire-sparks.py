import pyxel
import random
import math

W, H = 180, 180
MAX_SPARKS = 800
SPAWN_COUNT = 2

class Spark:
    def __init__(self, x, y):
        self.angle = math.radians(90 + random.uniform(-20, 20))
        self.speed = random.uniform(.2, 3.5)
        self.x = x
        self.y = y
        self.life = random.randint(30, 80)
        self.size = random.randint(1, 3)
        self.color = random.choice([8, 9, 10])  # 赤, オレンジ, 黄色の単色

    def update(self):
        # 角度にtanで揺れ
        self.angle += math.tan(random.uniform(-0.8, 0.8)) * 0.5
        dx = math.cos(self.angle) * self.speed
        dy = -math.sin(self.angle) * self.speed
        self.x += dx
        self.y += dy
        self.life -= 1

    def draw(self):
        # 4x4の単色ドット
        for i in range(self.size):
            for j in range(self.size):
                px = int(self.x) + i
                py = int(self.y) + j
                if 0 <= px < W and 0 <= py < H:
                    pyxel.pset(px, py, self.color)

class App:
    def __init__(self):
        pyxel.init(W, H, title="Fire Sparks")
        self.sparks = []
        pyxel.run(self.update, self.draw)

    def spawn(self, n):
        for _ in range(n):
            if len(self.sparks) < MAX_SPARKS:
                x = random.randint(0, W)
                y = H - 5
                self.sparks.append(Spark(x, y))

    def update(self):
        # 自動生成
        self.spawn(SPAWN_COUNT)

        # スペースキーで追加生成
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.spawn(100)  # スペースで20個追加

        alive = []
        for s in self.sparks:
            s.update()
            if s.life > 0 and 0 <= s.x < W and 0 <= s.y < H:
                alive.append(s)
        self.sparks = alive


    def draw(self):
        pyxel.cls(0)  # 背景黒
        for s in self.sparks:
            s.draw()
        pyxel.text(4, 4, f"Sparks: {len(self.sparks)}", 7)
        pyxel.text(4, 12, "SPACE to spawn sparks", 7)

App()
