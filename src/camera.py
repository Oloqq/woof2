import pygame

class Camera:
    def __init__(self, x, y, zoom):
        self.x: float = x
        self.y: float = y
        self.zoom: float = zoom

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x = max(self.x - 10, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += 10
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y = max(self.y - 10, 0)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += 10
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.zoom = min(2, self.zoom + 0.1)
        if keys[pygame.K_MINUS]:
            self.zoom = max(0.5, self.zoom - 0.1)