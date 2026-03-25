import pygame, random, os, math, array

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# ---------------- WINDOW ----------------
W, H = 520, 720
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("2048")
clock = pygame.time.Clock()

PAD = 12
BEST_FILE = "best_score.txt"
GRID_SIZE = 4

# ---------------- COLORS ----------------
BG_TOP = (10, 19, 34)
BG_BOTTOM = (24, 44, 68)

GRID_BG = (17, 33, 54)
EMPTY = (42, 58, 76)

BOX_BG = (29, 58, 88)
BOX_SHADOW = (7, 16, 28)

BEST_GLOW = (116, 208, 255)

BTN_BG = (58, 157, 176)
BTN_HOVER = (86, 184, 202)

TILE_COLORS = {
    2: (92, 116, 146),
    4: (98, 136, 166),
    8: (74, 156, 156),
    16: (72, 170, 136),
    32: (98, 182, 112),
    64: (184, 160, 82),
    128: (196, 126, 82),
    256: (194, 104, 108),
    512: (162, 96, 174),
    1024: (118, 108, 208),
    2048: (224, 188, 86),
}

TEXT_DARK = (240, 246, 250)
WHITE = (245, 250, 250)
GOLD = (255, 215, 132)
PANEL_EDGE = (88, 168, 214)

FONT = pygame.font.SysFont("segoeui", 26, True)
BIG = pygame.font.SysFont("segoeui", 52, True)
SMALL = pygame.font.SysFont("segoeui", 16, True)

# ---------------- AUDIO ----------------
MOVE_SOUND = None
MERGE_SOUND = None
SPAWN_SOUND = None
BUTTON_SOUND = None
LOSE_SOUND = None
NEW_TILE_SOUND = None


def make_tone(freq=440, duration=0.08, volume=0.2, decay=8, vibrato=0.0):
    sample_rate = 44100
    n = int(sample_rate * duration)
    buf = array.array("h")
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-decay * t)
        f = freq * (1 + vibrato * math.sin(2 * math.pi * 6 * t))
        sample = int(32767 * volume * env * math.sin(2 * math.pi * f * t))
        buf.append(sample)
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_swell_tone(start_freq=320, end_freq=880, duration=0.12, volume=0.2, decay=6.5):
    sample_rate = 44100
    n = int(sample_rate * duration)
    buf = array.array("h")
    phase = 0.0
    for i in range(n):
        t = i / sample_rate
        blend = min(1.0, t / max(duration, 1e-6))
        freq = start_freq + (end_freq - start_freq) * (blend * blend)
        phase += 2 * math.pi * freq / sample_rate
        env = math.exp(-decay * t)
        shimmer = 0.22 * math.sin(phase * 1.5)
        sample = int(32767 * volume * env * (math.sin(phase) + shimmer) * 0.82)
        buf.append(max(-32767, min(32767, sample)))
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_chime(freqs, duration=0.12, volume=0.2):
    sample_rate = 44100
    n = int(sample_rate * duration)
    buf = array.array("h")
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-7 * t)
        s = 0.0
        for idx, f in enumerate(freqs):
            partial_vol = 1.0 / (1.2 + idx * 0.7)
            s += partial_vol * math.sin(2 * math.pi * f * t)
        s /= max(1, len(freqs))
        sample = int(32767 * volume * env * s)
        buf.append(max(-32767, min(32767, sample)))
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_noise_click(duration=0.03, volume=0.15, brightness=850):
    sample_rate = 44100
    n = int(sample_rate * duration)
    buf = array.array("h")
    last = 0.0
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-30 * t)
        rnd = random.uniform(-1.0, 1.0)
        last = 0.65 * last + 0.35 * rnd
        tone = math.sin(2 * math.pi * brightness * t) * 0.35
        s = (last * 0.65 + tone) * env
        sample = int(32767 * volume * s)
        buf.append(max(-32767, min(32767, sample)))
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_fall_tone(start_freq=420, end_freq=170, duration=0.35, volume=0.2):
    sample_rate = 44100
    n = int(sample_rate * duration)
    buf = array.array("h")
    for i in range(n):
        t = i / sample_rate
        p = t / max(duration, 1e-6)
        freq = start_freq + (end_freq - start_freq) * p
        env = math.exp(-3.8 * t)
        s1 = math.sin(2 * math.pi * freq * t)
        s2 = 0.35 * math.sin(2 * math.pi * (freq * 0.5) * t)
        sample = int(32767 * volume * env * (s1 + s2) * 0.75)
        buf.append(max(-32767, min(32767, sample)))
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_glass_ping(freq=1200, duration=0.11, volume=0.16):
    sample_rate = 44100
    n = int(sample_rate * duration)
    buf = array.array("h")
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-14 * t)
        s = (
            math.sin(2 * math.pi * freq * t)
            + 0.45 * math.sin(2 * math.pi * (freq * 1.49) * t)
            + 0.2 * math.sin(2 * math.pi * (freq * 2.03) * t)
        ) * 0.62
        sample = int(32767 * volume * env * s)
        buf.append(max(-32767, min(32767, sample)))
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_swipe_sound(start_freq=220, end_freq=560, duration=0.1, volume=0.16):
    sample_rate = 44100
    n = int(sample_rate * duration)
    buf = array.array("h")
    phase = 0.0
    noise = 0.0
    for i in range(n):
        t = i / sample_rate
        p = t / max(duration, 1e-6)
        freq = start_freq + (end_freq - start_freq) * (1 - (1 - p) * (1 - p))
        phase += 2 * math.pi * freq / sample_rate
        noise = 0.82 * noise + 0.18 * random.uniform(-1.0, 1.0)
        env = math.exp(-11.5 * t)
        tone = math.sin(phase) + 0.24 * math.sin(phase * 1.8)
        shimmer = noise * 0.34 + math.sin(2 * math.pi * 18 * t) * 0.08
        sample = int(32767 * volume * env * (tone * 0.76 + shimmer))
        buf.append(max(-32767, min(32767, sample)))
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_button_bloom(freqs=(520, 780, 1040), duration=0.16, volume=0.16):
    sample_rate = 44100
    n = int(sample_rate * duration)
    buf = array.array("h")
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-8.5 * t)
        s = 0.0
        for idx, freq in enumerate(freqs):
            drift = 1 + 0.02 * math.sin(2 * math.pi * (4 + idx) * t)
            s += math.sin(2 * math.pi * freq * drift * t) * (0.8 / (idx + 1))
        s += 0.12 * random.uniform(-1.0, 1.0)
        sample = int(32767 * volume * env * s * 0.52)
        buf.append(max(-32767, min(32767, sample)))
    return pygame.mixer.Sound(buffer=buf.tobytes())


def init_audio():
    global MOVE_SOUND, MERGE_SOUND, SPAWN_SOUND, BUTTON_SOUND, LOSE_SOUND, NEW_TILE_SOUND
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        MOVE_SOUND = make_swipe_sound(start_freq=170, end_freq=470, duration=0.11, volume=0.17)
        MERGE_SOUND = make_chime(freqs=[392, 587, 784, 1175], duration=0.22, volume=0.26)
        SPAWN_SOUND = make_glass_ping(freq=940, duration=0.1, volume=0.13)
        BUTTON_SOUND = make_button_bloom(freqs=(560, 860, 1260), duration=0.18, volume=0.16)
        LOSE_SOUND = make_fall_tone(start_freq=420, end_freq=118, duration=0.58, volume=0.24)
        NEW_TILE_SOUND = make_chime(freqs=[523, 784, 1175, 1568], duration=0.24, volume=0.26)
    except pygame.error:
        MOVE_SOUND = None
        MERGE_SOUND = None
        SPAWN_SOUND = None
        BUTTON_SOUND = None
        LOSE_SOUND = None
        NEW_TILE_SOUND = None


def play_sound(sound):
    if sound is not None:
        sound.play()


# ---------------- UTILS ----------------
def gradient():
    for y in range(H):
        t = y / max(1, H)
        r = BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t
        g = BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t
        b = BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (W, y))


def load_best():
    return int(open(BEST_FILE).read()) if os.path.exists(BEST_FILE) else 0


def save_best(v):
    open(BEST_FILE, "w").write(str(v))


def board_metrics(grid_size):
    size = min(W - 80, H - 260) // grid_size
    board_width = size * grid_size + PAD * (grid_size - 1)
    sx = (W - board_width) // 2
    sy = 190
    return sx, sy, size, board_width


def cell_center(r, c, grid_size):
    sx, sy, size, _ = board_metrics(grid_size)
    x = sx + c * (size + PAD) + size / 2
    y = sy + r * (size + PAD) + size / 2
    return x, y


# ---------------- ANIMATION STATE ----------------
score_scale = 1.0
best_glow_phase = 0.0
best_pop = 0.0
ui_time = 0.0
restart_scale = 1.0
restart_press = 0.0
board_pulse = 0.0
win_flash = 0.0
particles = []
popups = []

drawn_restart_btn = pygame.Rect(0, 0, 0, 0)
drawn_top_restart_btn = pygame.Rect(0, 0, 0, 0)


class Particle:
    def __init__(self, x, y, color, speed=3.0, size=4):
        ang = random.uniform(0, 2 * math.pi)
        mag = random.uniform(0.4, 1.0) * speed
        self.x = x
        self.y = y
        self.vx = math.cos(ang) * mag
        self.vy = math.sin(ang) * mag
        self.life = random.uniform(0.35, 0.7)
        self.max_life = self.life
        self.color = color
        self.size = random.uniform(size * 0.6, size * 1.3)

    def update(self, dt):
        self.life -= dt
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.04
        self.vx *= 0.98
        return self.life > 0

    def draw(self):
        a = max(0, min(255, int(255 * (self.life / self.max_life))))
        s = max(1, int(self.size * (0.5 + 0.5 * (self.life / self.max_life))))
        surf = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, a), (s, s), s)
        screen.blit(surf, (self.x - s, self.y - s))


class PopupText:
    def __init__(self, text, x, y, color=(255, 245, 185)):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.life = 0.9
        self.max_life = self.life
        self.vy = -1.25

    def update(self, dt):
        self.life -= dt
        self.y += self.vy
        return self.life > 0

    def draw(self):
        a = max(0, min(255, int(255 * (self.life / self.max_life))))
        txt = FONT.render(self.text, True, self.color)
        surf = pygame.Surface(txt.get_size(), pygame.SRCALPHA)
        surf.blit(txt, (0, 0))
        surf.set_alpha(a)
        screen.blit(surf, txt.get_rect(center=(self.x, self.y)))


def emit_particles(x, y, color=(190, 240, 255), count=8, speed=3.0, size=4):
    for _ in range(count):
        particles.append(Particle(x, y, color, speed=speed, size=size))


def emit_popup(text, x, y, color=(255, 245, 185)):
    popups.append(PopupText(text, x, y, color))


def draw_background_fx(t):
    for i in range(3):
        radius = 180 + i * 90
        x = int(W * (0.18 + i * 0.32) + math.sin(t * (0.22 + i * 0.06) + i) * 32)
        y = int(H * (0.12 + i * 0.25) + math.cos(t * (0.18 + i * 0.04) + i) * 22)
        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (90, 170, 220, 18 - i * 3), (radius, radius), radius)
        screen.blit(surf, (x - radius, y - radius))

    mesh = pygame.Surface((W, H), pygame.SRCALPHA)
    step = 64
    drift = int(t * 8) % step
    for x in range(-step, W + step, step):
        pygame.draw.line(mesh, (255, 255, 255, 5), (x + drift, 0), (x + drift, H), 1)
    for y in range(-step, H + step, step):
        pygame.draw.line(mesh, (255, 255, 255, 4), (0, y + drift), (W, y + drift), 1)
    screen.blit(mesh, (0, 0))

    for i in range(10):
        px = int((i * 91 + t * (10 + i % 3 * 3)) % (W + 40) - 20)
        py = int((i * 67 + t * (7 + i % 4 * 2)) % (H + 40) - 20)
        spark = pygame.Surface((18, 18), pygame.SRCALPHA)
        pygame.draw.circle(spark, (255, 255, 255, 28), (9, 9), 3)
        pygame.draw.circle(spark, (255, 255, 255, 70), (9, 9), 1)
        screen.blit(spark, (px, py))


def draw_vignette():
    vignette = pygame.Surface((W, H), pygame.SRCALPHA)
    pygame.draw.rect(vignette, (0, 0, 0, 28), vignette.get_rect(), width=36, border_radius=24)
    for i in range(5):
        inset = i * 16
        alpha = 6 + i * 3
        pygame.draw.rect(vignette, (4, 10, 18, alpha), (inset, inset, W - inset * 2, H - inset * 2), width=14, border_radius=34)
    screen.blit(vignette, (0, 0))


def draw_panel(rect, fill=(14, 43, 74), border=PANEL_EDGE, alpha=235, shine_phase=0.0, radius=28):
    panel = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 0))
    for y in range(rect.h):
        blend = y / max(1, rect.h - 1)
        row = (
            int(fill[0] + 10 * (1 - blend)),
            int(fill[1] + 18 * (1 - blend)),
            int(fill[2] + 28 * blend),
            alpha,
        )
        pygame.draw.line(panel, row, (0, y), (rect.w, y))
    pygame.draw.rect(panel, (*border, min(255, alpha)), panel.get_rect(), 2, border_radius=radius)

    glow = pygame.Surface((rect.w + 38, rect.h + 38), pygame.SRCALPHA)
    pygame.draw.rect(glow, (120, 205, 255, 14), glow.get_rect(), border_radius=radius + 16)
    screen.blit(glow, (rect.x - 19, rect.y - 19))
    screen.blit(panel, rect.topleft)

    sheen = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    sweep_x = int((math.sin(shine_phase) * 0.5 + 0.5) * (rect.w + 50)) - 50
    pygame.draw.rect(sheen, (255, 255, 255, 14), (sweep_x, 0, 34, rect.h), border_radius=18)
    pygame.draw.rect(sheen, (255, 255, 255, 12), (12, 8, rect.w - 24, 10), border_radius=12)
    screen.blit(sheen, rect.topleft)


def tint(color, amount):
    return tuple(max(0, min(255, int(c + (255 - c) * amount))) for c in color)


def shade(color, amount):
    return tuple(max(0, min(255, int(c * (1 - amount)))) for c in color)


def rounded_gradient(size, top_color, bottom_color, radius, alpha=255):
    w, h = size
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    for y in range(h):
        blend = y / max(1, h - 1)
        row = (
            int(top_color[0] + (bottom_color[0] - top_color[0]) * blend),
            int(top_color[1] + (bottom_color[1] - top_color[1]) * blend),
            int(top_color[2] + (bottom_color[2] - top_color[2]) * blend),
            alpha,
        )
        pygame.draw.line(surf, row, (0, y), (w, y))

    mask = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h), border_radius=radius)
    surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return surf


def draw_ui_button(rect, label, hover=False, press=0.0, phase=0.0, fill=BTN_BG, hover_fill=BTN_HOVER, style="glow"):
    scale = 1.0 + (0.028 if hover else 0.0) - 0.05 * press
    scale += 0.008 * math.sin(phase * 1.4)
    btn = rect.inflate(int(rect.w * (scale - 1)), int(rect.h * (scale - 1)))
    front = btn.move(0, -int(3 * press))
    shadow = front.move(0, 7)
    pygame.draw.rect(screen, (7, 16, 28), shadow, border_radius=20)

    aura = pygame.Surface((front.w + 34, front.h + 34), pygame.SRCALPHA)
    glow_color = (115, 205, 232, 22 if hover else 10)
    pygame.draw.rect(aura, glow_color, aura.get_rect(), border_radius=26)
    screen.blit(aura, (front.x - 17, front.y - 17))

    fill_color = hover_fill if hover else fill
    face = rounded_gradient(
        (front.w, front.h),
        tint(fill_color, 0.14),
        shade(fill_color, 0.08),
        20,
    )
    screen.blit(face, front.topleft)
    pygame.draw.rect(screen, (220, 242, 248), front, 1, border_radius=20)

    sheen = pygame.Surface((front.w, front.h), pygame.SRCALPHA)
    slide = int((math.sin(phase * 1.2) * 0.5 + 0.5) * (front.w + 60)) - 60
    pygame.draw.rect(sheen, (255, 255, 255, 16), (slide, 0, 46, front.h), border_radius=16)
    pygame.draw.rect(sheen, (255, 255, 255, 14), (8, 6, front.w - 16, 8), border_radius=10)
    screen.blit(sheen, front.topleft)

    text = SMALL.render(label, True, WHITE)
    screen.blit(text, text.get_rect(center=front.center))
    return front


def draw_box(x, y, w, h, title, value, scale=1.0, glow=False, float_off=0, sheen_phase=0.0):
    box_rect = pygame.Rect(x, y, w, h)
    box_rect.center = (x + w // 2, y + h // 2)
    box_rect.width = int(w * scale)
    box_rect.height = int(h * scale)
    box_rect.y += int(float_off)

    shadow = pygame.Rect(box_rect.x, box_rect.y + 10, box_rect.w, box_rect.h)
    pygame.draw.rect(screen, BOX_SHADOW, shadow, border_radius=22)
    box_fill = rounded_gradient(
        (box_rect.w, box_rect.h),
        tint(BOX_BG, 0.12),
        shade(BOX_BG, 0.1),
        22,
    )
    screen.blit(box_fill, box_rect.topleft)
    head_band = pygame.Rect(box_rect.x, box_rect.y, box_rect.w, max(16, box_rect.h // 3))
    pygame.draw.rect(screen, tint(BOX_BG, 0.1), head_band, border_radius=22)
    pygame.draw.rect(screen, tint(BOX_BG, 0.36), box_rect, 1, border_radius=22)

    if glow:
        glow_surf = pygame.Surface((box_rect.w + 12, box_rect.h + 12), pygame.SRCALPHA)
        alpha = int(38 + 22 * math.sin(best_glow_phase))
        pygame.draw.rect(glow_surf, (*BEST_GLOW, alpha), glow_surf.get_rect(), border_radius=26)
        screen.blit(glow_surf, (box_rect.x - 6, box_rect.y - 6))

    sheen = pygame.Surface((box_rect.w, box_rect.h), pygame.SRCALPHA)
    sweep_x = int((math.sin(sheen_phase) * 0.5 + 0.5) * (box_rect.w + 36)) - 36
    pygame.draw.rect(sheen, (255, 255, 255, 14), (sweep_x, 0, 26, box_rect.h), border_radius=16)
    pygame.draw.rect(sheen, (255, 255, 255, 12), (8, 6, box_rect.w - 16, 10), border_radius=12)
    screen.blit(sheen, box_rect.topleft)

    title_s = SMALL.render(title, True, (180, 225, 245))
    val_s = FONT.render(str(value), True, WHITE)
    screen.blit(title_s, title_s.get_rect(center=(box_rect.centerx, box_rect.y + 18)))
    val_shadow = FONT.render(str(value), True, (14, 28, 52))
    screen.blit(val_shadow, val_shadow.get_rect(center=(box_rect.centerx, box_rect.y + box_rect.h // 2 + 14)))
    screen.blit(val_s, val_s.get_rect(center=(box_rect.centerx, box_rect.y + box_rect.h // 2 + 11)))


# ---------------- TILE ----------------
class Tile:
    def __init__(self, value, r, c):
        self.value = value
        self.r, self.c = r, c
        self.x = self.tx = 0
        self.y = self.ty = 0
        self.size = 0
        self.scale = 0
        self.spawn = True
        self.pulse = 0
        self.wobble = random.uniform(0, 7)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.trail = []
        self.flash = 0.0

    def move_to(self, x, y):
        self.tx, self.ty = x, y

    def merge(self):
        self.pulse = 0.28
        self.flash = 1.0

    def update(self, dt):
        move_blend = min(0.92, dt * 42.0)
        prev_x, prev_y = self.x, self.y
        self.x += (self.tx - self.x) * move_blend
        self.y += (self.ty - self.y) * move_blend
        self.vel_x = self.x - prev_x
        self.vel_y = self.y - prev_y
        if abs(self.tx - self.x) < 0.2 and abs(self.vel_x) < 0.2:
            self.x = self.tx
            self.vel_x = 0.0
        if abs(self.ty - self.y) < 0.2 and abs(self.vel_y) < 0.2:
            self.y = self.ty
            self.vel_y = 0.0
        self.wobble += dt * 5.0
        speed = math.hypot(self.vel_x, self.vel_y)
        if speed > 0.08:
            self.trail.append((self.x + self.size * 0.5, self.y + self.size * 0.5, min(1.0, speed / 8.0)))
        if len(self.trail) > 2:
            self.trail.pop(0)
        if self.flash > 0:
            self.flash *= max(0.68, 1.0 - dt * 14.0)

        if self.spawn:
            self.scale += (1 - self.scale) * min(0.72, dt * 30.0)
            if self.scale > 0.99:
                self.scale = 1
                self.spawn = False
        elif self.pulse > 0:
            self.scale = 1 + self.pulse
            self.pulse *= max(0.5, 1.0 - dt * 22.0)
        else:
            self.scale += (1 - self.scale) * min(0.42, dt * 16.0)

    def draw(self):
        s = self.size * self.scale
        lift = math.sin(self.wobble) * 0.18
        draw_w = s
        draw_h = s
        rect = pygame.Rect(
            self.x + (self.size - draw_w) / 2,
            self.y + (self.size - draw_h) / 2 + lift,
            draw_w,
            draw_h,
        )
        shadow = pygame.Rect(rect.x, rect.y + 6, rect.w, rect.h)
        for idx, (tx, ty, power) in enumerate(self.trail):
            radius = max(3, int(self.size * (0.06 - idx * 0.008)))
            trail = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
            alpha = max(6, int(14 * power * (idx + 1) / max(1, len(self.trail))))
            pygame.draw.circle(trail, (190, 235, 255, alpha), (radius * 2, radius * 2), radius)
            screen.blit(trail, (tx - radius * 2, ty - radius * 2))

        pygame.draw.rect(screen, (5, 12, 20), shadow, border_radius=18)
        tile_color = TILE_COLORS.get(self.value, (40, 125, 190))
        glow = pygame.Surface((rect.w + 30, rect.h + 30), pygame.SRCALPHA)
        glow_alpha = 14 + int(self.flash * 48)
        pygame.draw.rect(glow, (*tint(tile_color, 0.2), glow_alpha), glow.get_rect(), border_radius=24)
        screen.blit(glow, (rect.x - 15, rect.y - 15))
        tile_fill = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        top_color = tint(tile_color, 0.14)
        bottom_color = shade(tile_color, 0.14)
        for y in range(rect.h):
            blend = y / max(1, rect.h - 1)
            row = (
                int(top_color[0] + (bottom_color[0] - top_color[0]) * blend),
                int(top_color[1] + (bottom_color[1] - top_color[1]) * blend),
                int(top_color[2] + (bottom_color[2] - top_color[2]) * blend),
                255,
            )
            pygame.draw.line(tile_fill, row, (0, y), (rect.w, y))
        screen.blit(tile_fill, rect.topleft)
        pygame.draw.rect(screen, tint(tile_color, 0.34), rect, 1, border_radius=18)

        sheen = pygame.Surface((int(rect.w), int(rect.h)), pygame.SRCALPHA)
        pygame.draw.rect(sheen, (255, 255, 255, 18), (10, 8, rect.w - 20, 10), border_radius=10)
        sweep_x = int((math.sin(self.wobble * 0.45) * 0.5 + 0.5) * (rect.w + 34)) - 34
        pygame.draw.rect(sheen, (255, 255, 255, 10), (sweep_x, 0, 20, rect.h), border_radius=18)
        pygame.draw.ellipse(sheen, (255, 255, 255, 12), (rect.w * 0.2, rect.h * 0.56, rect.w * 0.6, rect.h * 0.14))
        pygame.draw.ellipse(sheen, (*tint(tile_color, 0.5), 24), (rect.w * 0.12, rect.h * 0.14, rect.w * 0.76, rect.h * 0.24))
        screen.blit(sheen, rect.topleft)

        if self.flash > 0:
            burst = pygame.Surface((rect.w + 20, rect.h + 20), pygame.SRCALPHA)
            pygame.draw.rect(burst, (255, 255, 255, int(52 * self.flash)), burst.get_rect(), 3, border_radius=22)
            screen.blit(burst, (rect.x - 10, rect.y - 10))
        font = FONT if self.value < 1024 else pygame.font.SysFont("segoeui", 22, True)
        value_str = str(self.value)
        txt = font.render(value_str, True, TEXT_DARK)
        txt_shadow = font.render(value_str, True, (8, 14, 22))
        screen.blit(txt_shadow, txt_shadow.get_rect(center=(rect.centerx, rect.centery + 2)))
        screen.blit(txt, txt.get_rect(center=(rect.centerx, rect.centery)))


# ---------------- GAME ----------------
class Game:
    def __init__(self, grid_size):
        self.best = load_best()
        self.grid_size = grid_size
        self.restart()

    def restart(self):
        global board_pulse
        self.score = 0
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.tiles = {}
        self.over = False
        self.won = False
        self.win_fx_done = False
        self.unlocked_values = {2, 4}
        board_pulse = 0.0
        self.spawn()
        self.spawn()

    def spawn(self):
        empty = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if self.grid[r][c] == 0]
        if not empty:
            return
        r, c = random.choice(empty)
        val = 4 if random.random() < 0.12 else 2
        self.grid[r][c] = val
        self.tiles[(r, c)] = Tile(val, r, c)
        x, y = cell_center(r, c, self.grid_size)
        emit_particles(x, y, color=(200, 245, 255), count=8, speed=2.2, size=3)
        play_sound(SPAWN_SOUND)

    def move(self, dx, dy):
        global score_scale, best_pop, board_pulse
        moved = False
        merged = set()
        merged_this_move = False
        unlocked_new_value = False

        order = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size)]
        if dx == 1:
            order.sort(key=lambda x: -x[1])
        if dy == 1:
            order.sort(key=lambda x: -x[0])

        for r, c in order:
            if self.grid[r][c] == 0:
                continue
            cr, cc = r, c
            while True:
                nr, nc = cr + dy, cc + dx
                if not (0 <= nr < self.grid_size and 0 <= nc < self.grid_size):
                    break
                if self.grid[nr][nc] != 0:
                    break
                cr, cc = nr, nc

            if (cr, cc) != (r, c):
                self.grid[cr][cc] = self.grid[r][c]
                self.grid[r][c] = 0
                self.tiles[(cr, cc)] = self.tiles.pop((r, c))
                moved = True
                r, c = cr, cc

            nr, nc = r + dy, c + dx
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                if self.grid[nr][nc] == self.grid[r][c] and (nr, nc) not in merged:
                    self.grid[nr][nc] *= 2
                    self.grid[r][c] = 0
                    self.tiles[(nr, nc)].value *= 2
                    self.tiles[(nr, nc)].merge()
                    self.tiles.pop((r, c))
                    merged.add((nr, nc))
                    merged_this_move = True
                    x, y = cell_center(nr, nc, self.grid_size)
                    emit_particles(x, y, color=(255, 245, 190), count=15, speed=3.6, size=5)
                    emit_popup(f"+{self.grid[nr][nc]}", x, y - 18)
                    if self.grid[nr][nc] not in self.unlocked_values:
                        self.unlocked_values.add(self.grid[nr][nc])
                        unlocked_new_value = True
                    if self.grid[nr][nc] == 2048 and not self.won:
                        self.won = True
                    self.score += self.grid[nr][nc]
                    score_scale = 1.25
                    board_pulse = 0.22
                    old_best = self.best
                    self.best = max(self.best, self.score)
                    if self.best > old_best:
                        best_pop = 0.26
                    save_best(self.best)
                    moved = True

        if moved:
            if unlocked_new_value:
                play_sound(NEW_TILE_SOUND)
            else:
                play_sound(MERGE_SOUND if merged_this_move else MOVE_SOUND)
            if self.won:
                self.trigger_win_fx()
            else:
                self.spawn()
                self.check_over()
        return moved

    def trigger_win_fx(self):
        global win_flash
        if self.win_fx_done:
            return
        self.win_fx_done = True
        win_flash = 1.0
        cx, cy = W // 2, H // 2
        emit_particles(cx, cy, color=(255, 230, 120), count=80, speed=5.0, size=5)
        emit_particles(cx, cy, color=(120, 235, 255), count=60, speed=4.2, size=4)
        emit_popup("2048!", cx, cy - 54, color=(255, 245, 160))
        play_sound(NEW_TILE_SOUND)

    def check_over(self):
        if self.won:
            return
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r][c] == 0:
                    return
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nr, nc = r + dy, c + dx
                    if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and self.grid[nr][nc] == self.grid[r][c]:
                        return
        self.over = True
        play_sound(LOSE_SOUND)

    def draw(self, dt):
        sx, sy, size, board_width = board_metrics(self.grid_size)

        pulse_expand = int(board_pulse * 4)
        board_outer = pygame.Rect(sx - 20 - pulse_expand, sy - 20 - pulse_expand, board_width + 40 + pulse_expand * 2, board_width + 40 + pulse_expand * 2)
        board_inner = pygame.Rect(sx - 12, sy - 12, board_width + 24, board_width + 24)
        aura = pygame.Surface((board_outer.w + 60, board_outer.h + 60), pygame.SRCALPHA)
        aura_alpha = int(12 + 6 * math.sin(ui_time * 1.2) + board_pulse * 24)
        pygame.draw.ellipse(aura, (98, 182, 228, max(0, min(255, aura_alpha))), aura.get_rect())
        screen.blit(aura, (board_outer.x - 30, board_outer.y - 30))

        board_shadow = board_outer.move(0, 18)
        pygame.draw.rect(screen, (6, 14, 24), board_shadow, border_radius=34)
        pygame.draw.rect(screen, (13, 25, 42), board_outer, border_radius=30)

        board_fill = pygame.Surface((board_inner.w, board_inner.h), pygame.SRCALPHA)
        for y2 in range(board_inner.h):
            blend = y2 / max(1, board_inner.h - 1)
            row = (
                int(tint(GRID_BG, 0.07)[0] + (shade(GRID_BG, 0.12)[0] - tint(GRID_BG, 0.07)[0]) * blend),
                int(tint(GRID_BG, 0.07)[1] + (shade(GRID_BG, 0.12)[1] - tint(GRID_BG, 0.07)[1]) * blend),
                int(tint(GRID_BG, 0.07)[2] + (shade(GRID_BG, 0.12)[2] - tint(GRID_BG, 0.07)[2]) * blend),
                255,
            )
            pygame.draw.line(board_fill, row, (0, y2), (board_inner.w, y2))
        screen.blit(board_fill, board_inner.topleft)
        pygame.draw.rect(screen, tint(GRID_BG, 0.26), board_inner, 1, border_radius=28)

        board_sheen = pygame.Surface((board_inner.w, board_inner.h), pygame.SRCALPHA)
        sweep_x = int((math.sin(ui_time * 0.8) * 0.5 + 0.5) * (board_inner.w + 90)) - 90
        pygame.draw.rect(board_sheen, (255, 255, 255, 10), (sweep_x, 0, 72, board_inner.h), border_radius=24)
        pygame.draw.ellipse(board_sheen, (255, 255, 255, 10), (24, 14, board_inner.w - 48, 22))
        screen.blit(board_sheen, board_inner.topleft)

        old_clip = screen.get_clip()
        screen.set_clip(board_inner.inflate(-8, -8))
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x = sx + c * (size + PAD)
                y = sy + r * (size + PAD)
                slot_shadow = pygame.Rect(x, y + 5, size, size)
                pygame.draw.rect(screen, (7, 17, 28), slot_shadow, border_radius=20)
                slot = pygame.Rect(x, y, size, size)
                slot_fill = pygame.Surface((size, size), pygame.SRCALPHA)
                for y2 in range(size):
                    blend = y2 / max(1, size - 1)
                    row = (
                        int(tint(EMPTY, 0.04)[0] + (shade(EMPTY, 0.1)[0] - tint(EMPTY, 0.04)[0]) * blend),
                        int(tint(EMPTY, 0.04)[1] + (shade(EMPTY, 0.1)[1] - tint(EMPTY, 0.04)[1]) * blend),
                        int(tint(EMPTY, 0.04)[2] + (shade(EMPTY, 0.1)[2] - tint(EMPTY, 0.04)[2]) * blend),
                        255,
                    )
                    pygame.draw.line(slot_fill, row, (0, y2), (size, y2))
                screen.blit(slot_fill, slot.topleft)
                pygame.draw.rect(screen, (220, 232, 238), slot, 1, border_radius=20)
                if (r, c) in self.tiles:
                    t = self.tiles[(r, c)]
                    t.size = size
                    t.move_to(x, y)
                    t.update(dt)
                    t.draw()
        screen.set_clip(old_clip)


def draw_particles_and_popups():
    alive = []
    for p in particles:
        if p.update(1 / 60):
            p.draw()
            alive.append(p)
    particles[:] = alive

    text_alive = []
    for t in popups:
        if t.update(1 / 60):
            t.draw()
            text_alive.append(t)
    popups[:] = text_alive


def draw_overlay_card(title_text, subtitle_text, y_center, phase, accent=(255, 230, 150)):
    card = pygame.Rect(W // 2 - 190, y_center - 118, 380, 236)
    draw_panel(card, fill=(15, 28, 46), border=(112, 166, 205), alpha=242, shine_phase=phase, radius=30)

    glow = pygame.Surface((card.w + 60, card.h + 60), pygame.SRCALPHA)
    pygame.draw.ellipse(glow, (*accent, 18), glow.get_rect())
    screen.blit(glow, (card.x - 30, card.y - 30))

    title = BIG.render(title_text, True, WHITE)
    pulse = 1.0 + 0.025 * math.sin(phase * 2.0)
    title = pygame.transform.smoothscale(title, (int(title.get_width() * pulse), int(title.get_height() * pulse)))
    screen.blit(title, title.get_rect(center=(card.centerx, card.y + 72)))

    subtitle = FONT.render(subtitle_text, True, (230, 240, 245))
    screen.blit(subtitle, subtitle.get_rect(center=(card.centerx, card.y + 136)))
    return card


# ---------------- MAIN LOOP ----------------
init_audio()

game = Game(GRID_SIZE)
restart_btn = pygame.Rect(0, 0, 180, 48)

running = True
while running:
    dt = clock.tick(60) / 1000.0
    W, H = screen.get_size()
    gradient()
    draw_background_fx(ui_time)

    ui_time += 4.8 * dt
    score_scale += (1 - score_scale) * 0.15
    best_glow_phase += 0.08
    if best_pop > 0:
        best_pop *= 0.86
    if restart_press > 0:
        restart_press *= 0.84
    if board_pulse > 0:
        board_pulse *= 0.88
    if win_flash > 0:
        win_flash *= 0.92

    if game is not None:
        header_panel = pygame.Rect(20, 20, W - 40, 136)
        draw_panel(header_panel, fill=(15, 30, 50), border=(80, 150, 196), shine_phase=ui_time * 0.9, radius=26)

        title_phase = 1.0 + 0.008 * math.sin(ui_time * 1.4)
        title = BIG.render("2048", True, WHITE)
        title = pygame.transform.smoothscale(title, (int(title.get_width() * title_phase), int(title.get_height() * title_phase)))
        screen.blit(title, (34, 34))

        accent = SMALL.render("Classic mode", True, (214, 224, 230))
        screen.blit(accent, (38, 92))
        accent_line_w = 72 + int(4 * math.sin(ui_time * 1.8))
        pygame.draw.line(screen, (214, 224, 230), (38, 114), (38 + accent_line_w, 114), 2)

        score_box_scale = score_scale * (1 + 0.008 * math.sin(ui_time * 1.4))
        best_box_scale = (1 + best_pop) * (1 + 0.008 * math.sin(ui_time * 1.0 + 1.7))
        draw_box(190, 30, 120, 60, "SCORE", game.score, scale=score_box_scale, float_off=0.8 * math.sin(ui_time * 1.0), sheen_phase=ui_time * 1.2)
        draw_box(320, 30, 150, 60, "BEST", game.best, scale=best_box_scale, glow=True, float_off=1.2 * math.sin(ui_time * 0.9 + 0.8), sheen_phase=ui_time * 1.0 + 1.3)

        top_restart = pygame.Rect(W - 148, 100, 116, 38)
        top_hover = top_restart.collidepoint(pygame.mouse.get_pos())
        drawn_top_restart_btn = draw_ui_button(
            top_restart,
            "RESTART",
            hover=top_hover,
            press=restart_press,
            phase=ui_time * 1.4 + 1.7,
            fill=(50, 140, 160),
            hover_fill=(74, 167, 190),
            style="glow",
        )

        game.draw(dt)
        draw_particles_and_popups()

        if game.won:
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            win_alpha = int(84 + 18 * math.sin(ui_time * 2.0) + win_flash * 72)
            overlay.fill((16, 22, 32, max(80, min(180, win_alpha))))
            screen.blit(overlay, (0, 0))
            draw_overlay_card("YOU WIN!", f"Score {game.score}", H // 2 - 10, ui_time * 1.4, accent=(255, 215, 140))

            restart_btn.center = (W // 2, H // 2 + 86)
            hover = restart_btn.collidepoint(pygame.mouse.get_pos())
            target_restart_scale = 1.10 if hover else 1.0
            restart_scale += (target_restart_scale - restart_scale) * 0.2
            base = restart_btn.inflate(int(restart_btn.w * (restart_scale - 1)), int(restart_btn.h * (restart_scale - 1)))
            drawn_restart_btn = draw_ui_button(
                base,
                "PLAY AGAIN",
                hover=hover,
                press=restart_press,
                phase=ui_time * 1.3,
                fill=(58, 157, 176),
                hover_fill=(86, 184, 202),
                style="glow",
            )
        elif game.over:
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((8, 12, 20, 150))
            screen.blit(overlay, (0, 0))
            draw_overlay_card("GAME OVER", f"Best {game.best}", H // 2 - 16, ui_time * 1.2, accent=(180, 210, 240))

            restart_btn.center = (W // 2, H // 2 + 76)
            hover = restart_btn.collidepoint(pygame.mouse.get_pos())
            target_restart_scale = 1.10 if hover else 1.0
            restart_scale += (target_restart_scale - restart_scale) * 0.2
            base = restart_btn.inflate(int(restart_btn.w * (restart_scale - 1)), int(restart_btn.h * (restart_scale - 1)))
            drawn_restart_btn = draw_ui_button(
                base,
                "RESTART",
                hover=hover,
                press=restart_press,
                phase=ui_time * 1.3,
                fill=(58, 157, 176),
                hover_fill=(86, 184, 202),
                style="glow",
            )
        else:
            drawn_restart_btn = pygame.Rect(0, 0, 0, 0)

    draw_vignette()
    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if game is not None:
                if e.key == pygame.K_r:
                    restart_press = 1.0
                    game.restart()
                    play_sound(BUTTON_SOUND)
                if not game.over and not game.won:
                    if e.key == pygame.K_LEFT:
                        game.move(-1, 0)
                    if e.key == pygame.K_RIGHT:
                        game.move(1, 0)
                    if e.key == pygame.K_UP:
                        game.move(0, -1)
                    if e.key == pygame.K_DOWN:
                        game.move(0, 1)

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if game is not None:
                if drawn_top_restart_btn.collidepoint(e.pos):
                    restart_press = 1.0
                    play_sound(BUTTON_SOUND)
                    game.restart()
                elif (game.over or game.won) and drawn_restart_btn.collidepoint(e.pos):
                    restart_press = 1.0
                    play_sound(BUTTON_SOUND)
                    game.restart()

pygame.quit()
