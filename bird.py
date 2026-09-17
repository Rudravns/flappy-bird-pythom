import pygame


class bird:
    def __init__(self, starting_point=None):
        if starting_point is None:
            starting_point = pygame.Vector2(100, 250)

        self.radius = 18
        self.screen = pygame.display.get_surface()
        self.color = (255, 216, 0)
        self.pos = pygame.Vector2(starting_point)
        self.jump_power = 450
        self.gravity = 1300
        self.vel = pygame.Vector2(0, 0)

    def draw(self):
        center = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(self.screen, self.color, center, self.radius)

        # small eye to make the bird look more like a real bird
        eye_center = (int(self.pos.x + 6), int(self.pos.y - 5))
        pygame.draw.circle(self.screen, (255, 255, 255), eye_center, 4)
        pygame.draw.circle(self.screen, (0, 0, 0), (int(self.pos.x + 8), int(self.pos.y - 5)), 2)

    def update(self, dt: float, jump: bool = False, gravity: float | None = None):
        if gravity is None:
            gravity = self.gravity

        if jump:
            self.vel.y = -self.jump_power
        else:
            self.vel.y += gravity * dt

        self.pos += self.vel * dt

    