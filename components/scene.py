import typing
import pygame

class Scene:
    def __init__(self) -> None:
        pass
    def input(self, event: pygame.event.Event) -> None:
        pass
    def update(self) -> None:
        pass
    def draw(self, screen: pygame.surface.Surface) -> None:
        pass
    def onEnter(self) -> None:
        pass
    def onExit(self) -> None:
        pass

class SceneManager:
    _instance = None

    def __init__(self) -> None:
        SceneManager._instance = self

        self.scenes: typing.List[Scene] = []

    def isEmpty(self) -> bool:
        return len(self.scenes) == 0

    def input(self, event: pygame.event.Event) -> None:
        if len(self.scenes) <= 0: return

        self.scenes[-1].input(event)
        
    def update(self) -> None:
        if len(self.scenes) <= 0: return

        self.scenes[-1].update()

    def draw(self, screen: pygame.surface.Surface) -> None:
        if len(self.scenes) <= 0: return

        self.scenes[-1].draw(screen)

    def push(self, scene: Scene) -> None:
        if len(self.scenes) > 0: self.scenes[-1].onExit()

        self.scenes.append(scene)
        
        scene.onEnter()

    def clear(self) -> None:
        self.scenes = []

    @staticmethod
    def getInstance():
        if SceneManager._instance is None:
            SceneManager()
        return SceneManager._instance
