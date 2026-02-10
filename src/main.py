import pyxel
import math

WIDTH = 300
HEIGHT = 200
PLAYER_RADIUS = 3.5
TURN = 0.1
PAUSED = False



def draw_arrow(x1, y1, x2, y2, color):
    pyxel.line(x1, y1, x2, y2, color)

    angle = math.atan2(y2 - y1, x2 - x1)
    size = 5

    left = (
        x2 - size * math.cos(angle - 0.5),
        y2 - size * math.sin(angle - 0.5),
    )
    right = (
        x2 - size * math.cos(angle + 0.5),
        y2 - size * math.sin(angle + 0.5),
    )

    pyxel.line(x2, y2, int(left[0]), int(left[1]), color)
    pyxel.line(x2, y2, int(right[0]), int(right[1]), color)



class Player:
    def __init__(self, x, y, route, speed):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.route = route
        self.speed = speed
        self.target_index = 0

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.target_index = 0

    def update(self):
        if self.target_index >= len(self.route):
            return

        tx, ty = self.route[self.target_index]
        dx = tx - self.x
        dy = ty - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist < self.speed:
            self.x, self.y = tx, ty
            self.target_index += 1
        else:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

    def draw(self):
        pyxel.circ(self.x, self.y, PLAYER_RADIUS, 7)

    def draw_route(self):
        px, py = self.start_x, self.start_y
        for point in self.route:
            draw_arrow(px, py, point[0], point[1], 8)
            px, py = point



class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Football Play Animator")
        self.create_play()
        pyxel.run(self.update, self.draw)

    def create_play(self):
        self.players = []

        y_los = 140  # line of scrimmage

        # Quarterback
        self.players.append(
            Player(150, y_los, [(150, 170)], 1)
        )

        # Running Back
        self.players.append(
            Player(150, y_los + 15, [(120, 120), (150, 105)], 1.2)
        )

        # Wide Receivers
        self.players.append(
            Player(90, y_los, [(90, 50)], 1.5)   # Left go
        )
        self.players.append(
            Player(210, y_los, [(210, 110), (240, 110)], 1.2)  # Right out
        )

        self.players.append(Player(220, y_los + 5, [(220, 90), (200, 70)], 1.2)) #Post

        #Tight End
        self.players.append(Player(190, y_los + 5, [(180, y_los - 5), (100, y_los - 5)], 1.2)) #Drag
        
        # Offensive Line
        self.players.append(Player(120, y_los, [(120, y_los + 10)], 1.2))  # LT
        self.players.append(Player(135, y_los, [(135, y_los + 5)], 1.2))  # LG
        self.players.append(Player(150, y_los, [(150, y_los)], 1.2))  # C
        self.players.append(Player(165, y_los, [(165, y_los + 5)], 1.2))  # RG
        self.players.append(Player(180, y_los, [(180, y_los + 10)], 1.2))  # RT

    def update(self):
        global PAUSED

        if pyxel.btnp(pyxel.KEY_P):
            PAUSED = not PAUSED

        if PAUSED:
            return

        if pyxel.btnp(pyxel.KEY_R):
            for p in self.players:
                p.reset()

        for p in self.players:
            p.update()

    def draw_field(self):
        pyxel.cls(11)

        for y in range(20, HEIGHT, 20):
            pyxel.line(0, y, WIDTH, y, 3)

        pyxel.line(0, 140, WIDTH, 140, 0)

    def draw(self):
        self.draw_field()

        for p in self.players:
            p.draw_route()

    
        for p in self.players:
            p.draw()

        pyxel.text(5, 5, "R = Reset Play", 0)
        pyxel.text(5, 15, "P = Pause Play", 0)


App()