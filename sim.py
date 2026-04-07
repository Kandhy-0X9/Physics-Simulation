import pygame
import math

# Set up display
WIDTH, HEIGHT = 1200, 720
# Colors
BG = ("white")
pygame.init() # Initialize Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cannon Physics Simulation")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(BG)
    pygame.display.flip()

pygame.quit() # Quit Pygame