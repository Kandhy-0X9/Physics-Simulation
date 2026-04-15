import pygame
import math
import sys

# Set up vars
WIDTH, HEIGHT = 1200, 720
fps = 60
groundY = HEIGHT - 80
cannonX = 80
cannonY = groundY - 20
SCALE = 4 # 4 pixels is one meter
DT = 0.05 # Physics simulation fixed time step (seconds)
maxTrail = 200 # Maximum number of trail points to draw for a shot

# Colors
BG = (221, 224, 223) # pearl river/ whitish
gridColor = (50, 50, 50) # grey 
groundColor = (26, 42, 20) # dark green
grassColor = (45,74,34) # green
cannonColor = (138, 117, 96) # peach
wheelColor = (58, 42, 24) # brown
ballColor = (0, 0, 0) # black
trailColor = (255, 160, 60) # light orange
txtColor = (220, 220, 220) # gainsboro/ lightgray - primary txt color
mutedColor = (140, 140, 150) # secondary txt color
fireColor = (200, 75, 42) # highlight color for firing
borderColor = (50, 55, 75) # for UI separation
ghostColor = (150, 150, 255, 60) # ideal trail color with no air resistance
panelColor = (20, 24, 38) # side panel background

pygame.init()  # Initialize all imported pygame modules
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the main display surface
pygame.display.set_caption("Cannon Physics Simulation")  # Window title
clock = pygame.time.Clock()  # Clock to control frame rate

# fonts
fontSmall = pygame.font.SysFont("monospace", 13) # Small UI font
fontMedium = pygame.font.SysFont("monospace", 15, bold=True)  # Medium UI font
fontLarge = pygame.font.SysFont("monospace", 18, bold=True)  # Large UI font
fontTittle = pygame.font.SysFont("monospace", 22, bold=True)  # Title font

# functions
def simulate():
    print("nothing in here")

def drawGrid():
    print("nothing in here")

def drawGround():
    print("nothing in here")

def drawCannon():
    print("nothing in here")

def drawBall():
    print("nothing in here")

def drawPanel():
    print("nothing in here")

def drawGhost():
    print("nothing in here")

def showStats():
    print("nothing in here")

def main():
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        # Draw scene EVERY FRAME
        screen.fill(BG)
        # Update display
        pygame.display.flip()
    pygame.quit()

# run main loop
if __name__ == "__main__":
    main()