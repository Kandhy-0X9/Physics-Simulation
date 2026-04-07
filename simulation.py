import pygame
import math
import sys

# --- Constants ---
WIDTH, HEIGHT = 1200, 720
FPS = 60
GROUND_Y = HEIGHT - 80
CANNON_X = 80
CANNON_Y = GROUND_Y - 20
SCALE = 4          # pixels per meter
DT = 0.05          # simulation time step (seconds)
MAX_PTS = 200      # trail length

# --- Colors ---
BG         = (10, 14, 26)
GRID       = (255, 255, 255, 10)
GROUND_COL = (26, 42, 20)
GRASS_COL  = (45, 74, 34)
CANNON_COL = (138, 117, 96)
WHEEL_COL  = (58, 42, 24)
BALL_COL   = (50, 50, 50)
TRAIL_COL  = (255, 160, 60)
TEXT_COL   = (220, 220, 220)
MUTED_COL  = (140, 140, 150)
FIRE_COL   = (200, 75, 42)
GHOST_COL  = (150, 150, 255, 60)
PANEL_COL  = (20, 24, 38)
BORDER_COL = (50, 55, 75)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cannon Physics Simulation")
clock = pygame.time.Clock()
font_sm = pygame.font.SysFont("monospace", 13)
font_md = pygame.font.SysFont("monospace", 15, bold=True)
font_lg = pygame.font.SysFont("monospace", 18, bold=True)
font_title = pygame.font.SysFont("monospace", 22, bold=True)


def simulate(angle_deg, v0, g, k, dt=DT, max_steps=4000):
    """Simulate projectile and return list of (x, y) world coords."""
    rad = math.radians(angle_deg)
    vx = v0 * math.cos(rad)
    vy = v0 * math.sin(rad)
    x, y = 0.0, 0.0
    pts = [(x, y)]
    for _ in range(max_steps):
        speed = math.sqrt(vx**2 + vy**2)
        vx -= k * speed * vx * dt
        vy -= k * speed * vy * dt
        vy -= g * dt
        x += vx * dt
        y += vy * dt
        if y < 0 and len(pts) > 1:
            # Interpolate exact ground hit
            px, py = pts[-1]
            frac = -py / (y - py)
            x = px + frac * (x - px)
            y = 0.0
            pts.append((x, y))
            break
        pts.append((x, y))
    return pts


def world_to_screen(wx, wy):
    sx = int(CANNON_X + wx * SCALE)
    sy = int(GROUND_Y - wy * SCALE)
    return sx, sy


def draw_grid(surf):
    for x in range(0, WIDTH, 60):
        pygame.draw.line(surf, (30, 35, 55), (x, 0), (x, GROUND_Y))
    for y in range(GROUND_Y, 0, -60):
        pygame.draw.line(surf, (30, 35, 55), (0, y), (WIDTH, y))


def draw_ground(surf):
    pygame.draw.rect(surf, GROUND_COL, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    pygame.draw.line(surf, GRASS_COL, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)


def draw_cannon(surf, angle_deg):
    rad = math.radians(angle_deg)
    barrel_len = 44
    barrel_w = 10

    # Wheels
    for dx in (-18, 18):
        pygame.draw.circle(surf, WHEEL_COL, (CANNON_X + dx, CANNON_Y + 14), 8)
        pygame.draw.circle(surf, (80, 60, 40), (CANNON_X + dx, CANNON_Y + 14), 4)
    pygame.draw.rect(surf, WHEEL_COL, (CANNON_X - 20, CANNON_Y + 12, 40, 6))

    # Body
    pygame.draw.circle(surf, WHEEL_COL, (CANNON_X, CANNON_Y), 15)
    pygame.draw.circle(surf, (200, 168, 112), (CANNON_X, CANNON_Y), 10)

    # Barrel (rotated rect)
    end_x = CANNON_X + barrel_len * math.cos(rad)
    end_y = CANNON_Y - barrel_len * math.sin(rad)
    perp_x = barrel_w / 2 * math.sin(rad)
    perp_y = barrel_w / 2 * math.cos(rad)
    barrel_pts = [
        (CANNON_X - perp_x, CANNON_Y - perp_y),
        (CANNON_X + perp_x, CANNON_Y + perp_y),
        (end_x + perp_x, end_y + perp_y),
        (end_x - perp_x, end_y - perp_y),
    ]
    pygame.draw.polygon(surf, CANNON_COL, barrel_pts)
    pygame.draw.polygon(surf, WHEEL_COL, barrel_pts, 1)


def draw_ball(surf, ball):
    pts = ball["pts"]
    head = ball["head"]

    # Trail
    if ball["show_trail"] and head > 1:
        start = max(0, head - MAX_PTS)
        for i in range(start, head - 1):
            alpha = (i - start) / MAX_PTS
            col = (
                int(TRAIL_COL[0]),
                int(TRAIL_COL[1] * alpha),
                int(TRAIL_COL[2] * alpha * 0.3),
            )
            p1 = world_to_screen(*pts[i])
            p2 = world_to_screen(*pts[i + 1])
            pygame.draw.line(surf, col, p1, p2, 2)

    if not ball["done"]:
        sx, sy = world_to_screen(*pts[head])
        pygame.draw.circle(surf, BALL_COL, (sx, sy), 7)
        pygame.draw.circle(surf, (100, 100, 100), (sx - 2, sy - 2), 3)
    else:
        # Crater
        sx, sy = world_to_screen(*pts[-1])
        pygame.draw.ellipse(surf, (15, 25, 12), (sx - 10, sy - 4, 20, 8))


def draw_ghost(surf, pts):
    if len(pts) < 2:
        return
    for i in range(len(pts) - 1):
        p1 = world_to_screen(*pts[i])
        p2 = world_to_screen(*pts[i + 1])
        if 0 <= p1[0] < WIDTH and 0 <= p2[0] < WIDTH:
            pygame.draw.line(surf, (100, 100, 200), p1, p2, 1)


def draw_panel(surf, angle, vel, gravity, air_resistance, stats, show_trail, show_ghost):
    panel_x = WIDTH - 210
    pygame.draw.rect(surf, PANEL_COL, (panel_x - 8, 0, 218, HEIGHT))
    pygame.draw.line(surf, BORDER_COL, (panel_x - 8, 0), (panel_x - 8, HEIGHT), 1)

    y = 16
    title = font_title.render("CANNON SIM", True, (220, 200, 160))
    surf.blit(title, (panel_x, y))
    y += 34

    # Parameters
    params = [
        ("Angle",    f"{angle:.0f} deg",   "[<-] / [->]"),
        ("Velocity", f"{vel:.0f} m/s",     "A / D"),
        ("Gravity",  f"{gravity:.1f} m/s2","W / S"),
        ("Air Resistance", f"{air_resistance:.3f}", "Z / X"),
    ]
    for label, val, keys in params:
        pygame.draw.rect(surf, (28, 33, 50), (panel_x - 4, y - 2, 206, 38), border_radius=6)
        surf.blit(font_sm.render(label, True, MUTED_COL), (panel_x, y))
        surf.blit(font_md.render(val, True, TEXT_COL), (panel_x, y + 16))
        surf.blit(font_sm.render(keys, True, (80, 90, 110)), (panel_x + 110, y + 18))
        y += 46

    y += 4
    pygame.draw.line(surf, BORDER_COL, (panel_x - 4, y), (panel_x + 200, y))
    y += 12

    # Stats
    stat_labels = [
        ("Max height",   stats.get("max_h", "—")),
        ("Range",        stats.get("range", "—")),
        ("Flight time",  stats.get("time",  "—")),
        ("Impact speed", stats.get("imp_v", "—")),
    ]
    for label, val in stat_labels:
        surf.blit(font_sm.render(label, True, MUTED_COL), (panel_x, y))
        surf.blit(font_md.render(str(val), True, (180, 220, 180)), (panel_x, y + 14))
        y += 34

    y += 6
    pygame.draw.line(surf, BORDER_COL, (panel_x - 4, y), (panel_x + 200, y))
    y += 12

    # Toggles & keys
    controls = [
        (f"[T]Trail: {'ON' if show_trail else 'OFF'}", show_trail),
        (f"[G]Ghost(Path With No Drag): {'ON' if show_ghost else 'OFF'}", show_ghost),
    ]
    for txt, active in controls:
        col = (100, 200, 120) if active else (120, 120, 130)
        surf.blit(font_sm.render(txt, True, col), (panel_x, y))
        y += 20

    y += 8
    for txt in ["[SPACE] Fire!", "[C] Clear", "[Q/ESC] Quit"]:
        col = FIRE_COL if "SPACE" in txt else MUTED_COL
        surf.blit(font_sm.render(txt, True, col), (panel_x, y))
        y += 18


def compute_stats(pts):
    if not pts:
        return {}
    max_h = max(p[1] for p in pts)
    rng = pts[-1][0]
    time = len(pts) * DT
    if len(pts) >= 2:
        dx = pts[-1][0] - pts[-2][0]
        dy = pts[-1][1] - pts[-2][1]
        imp_v = math.sqrt((dx/DT)**2 + (dy/DT)**2)
    else:
        imp_v = 0
    return {
        "max_h": f"{max_h:.1f} m",
        "range": f"{rng:.1f} m",
        "time":  f"{time:.2f} s",
        "imp_v": f"{imp_v:.1f} m/s",
    }


def main():
    angle   = 45.0
    vel     = 60.0
    gravity = 9.8
    air_resistance = 0.0
    show_trail = True
    show_ghost = False

    balls = []
    stats = {}

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                if event.key == pygame.K_SPACE:
                    pts = simulate(angle, vel, gravity, air_resistance)
                    stats = compute_stats(pts)
                    if len(balls) > 6:
                        balls.pop(0)
                    balls.append({"pts": pts, "head": 0, "done": False, "show_trail": show_trail})
                if event.key == pygame.K_c:
                    balls.clear()
                    stats = {}
                if event.key == pygame.K_t:
                    show_trail = not show_trail
                if event.key == pygame.K_g:
                    show_ghost = not show_ghost

        # Held keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  or keys[pygame.K_LEFTBRACKET]:  angle = max(1,   angle - 0.5)
        if keys[pygame.K_RIGHT] or keys[pygame.K_RIGHTBRACKET]: angle = min(89,  angle + 0.5)
        if keys[pygame.K_a]: vel     = max(10,  vel - 0.5)
        if keys[pygame.K_d]: vel     = min(120, vel + 0.5)
        if keys[pygame.K_s]: gravity = max(1,   gravity - 0.05)
        if keys[pygame.K_w]: gravity = min(25,  gravity + 0.05)
        if keys[pygame.K_z]: air_resistance = max(0,   air_resistance - 0.001)
        if keys[pygame.K_x]: air_resistance = min(0.05, air_resistance + 0.001)

        # Advance ball animations
        for ball in balls:
            if not ball["done"]:
                ball["head"] = min(ball["head"] + 3, len(ball["pts"]) - 1)
                if ball["head"] >= len(ball["pts"]) - 1:
                    ball["done"] = True

        # Draw
        screen.fill(BG)
        draw_grid(screen)
        draw_ground(screen)

        if show_ghost:
            ghost_pts = simulate(angle, vel, gravity, 0)
            draw_ghost(screen, ghost_pts)

        for ball in balls:
            draw_ball(screen, ball)

        draw_cannon(screen, angle)
        draw_panel(screen, angle, vel, gravity, air_resistance, stats, show_trail, show_ghost)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()