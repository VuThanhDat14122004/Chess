import pygame

from game.Board import Board

pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])


def draw(display):
    display.fill((255, 255, 255))
    board.draw(display)
    pygame.display.update()


if __name__ == "__main__":
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.handle_click(mx, my)

        if board.is_in_checkmate("black"):
            print("White wins")
            running = False
        elif board.is_in_checkmate("white"):
            print("Black wins")
            running = False

        draw(screen)
