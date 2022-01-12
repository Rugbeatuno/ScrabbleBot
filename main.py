import pygame
pygame.init()

from visualization import Visualization


def main():
    clock = pygame.time.Clock()
    running = True

    display = Visualization()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                display.get_selected_tile(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    display.change_travel_direction()
                else:
                    display.get_pressed_key(event.key)


        display.refresh()
        pygame.display.update()
        clock.tick(15)

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()