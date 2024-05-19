import pygame


class DrawMenu:
    def __init__(self, canvas) -> None:
        self.screen = canvas
        self.start_time = 10

    def display(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 5, 5))

    def draw_count_down(self):
        pass
