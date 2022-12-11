import pygame
from components.scene import SceneManager
from modules.lobby.scenes import StartScene

import utils.constants as constants

pygame.init()
WINDOW = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption(constants.GAME)

SCENE_MANAGER = SceneManager.getInstance()
SCENE_MANAGER.push(StartScene())

def main():
    running: bool = True
    clock: pygame.time.Clock = pygame.time.Clock()

    while running:
        clock.tick(constants.FPS)

        running = not SCENE_MANAGER.isEmpty()

        for event in pygame.event.get():
            SCENE_MANAGER.input(event)

            if event.type == pygame.QUIT:
                running = False

        SCENE_MANAGER.update()
        SCENE_MANAGER.draw(WINDOW)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()