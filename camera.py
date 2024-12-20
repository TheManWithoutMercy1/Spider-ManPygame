import pygame
from abc import ABC, abstractmethod

vec = pygame.math.Vector2

class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.DISPLAY_W, self.DISPLAY_H = 800, 500
        self.CONST = vec(-self.DISPLAY_W / 2 + player.rect.w / 2, -self.DISPLAY_H / 2 + player.rect.h / 2)

    def setmethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()

    def apply(self, entity):
        return entity.rect.move(self.offset.x, self.offset.y)

class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass

class Follow(CamScroll):
    def __init__(self, camera, player):
        super().__init__(camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x - self.camera.DISPLAY_W / 2 + self.player.rect.w / 2) * 0.05
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y - self.camera.DISPLAY_H / 2 + self.player.rect.h / 2) * 0.05
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = max(self.camera.offset.x, self.camera.player.left_border - self.camera.CONST.x)
        self.camera.offset.x = min(self.camera.offset.x, self.camera.player.right_border - self.camera.DISPLAY_W)

class Border(CamScroll):
    def __init__(self, camera, player):
        super().__init__(camera, player)

    def scroll(self):
        self.camera.offset_float.x = self.player.rect.x + self.player.rect.w / 2 - self.camera.DISPLAY_W / 2
        self.camera.offset_float.y = self.player.rect.y + self.player.rect.h / 2 - self.camera.DISPLAY_H / 2
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = max(self.camera.offset.x, self.camera.player.left_border)
        self.camera.offset.x = min(self.camera.offset.x, self.camera.player.right_border - self.camera.DISPLAY_W)

class Auto(CamScroll):
    def __init__(self, camera, player):
        super().__init__(camera, player)

    def scroll(self):
        self.camera.offset.x += 1
