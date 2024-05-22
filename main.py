import pygame

from components.Game import Game

if __name__ == "__main__":
    width = 960
    height = 640
    square_size = 80
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    game = Game(width, height, square_size, screen)
    game.display()
    pygame.quit()
