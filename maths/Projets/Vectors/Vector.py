import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Fond d'écran avec a.png")

background = pygame.image.load("Vectors.png").convert()  # charge l’image

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Affiche l'image de fond
    screen.blit(background, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
