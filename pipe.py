import random
import pygame


class pipe:
    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        self.screen = pygame.display.get_surface()
        self.width = 70
        self.speed = 220
        self.gap_size = 180
        self.x = screen_width + 30
        self.gap_y = random.randint(120, screen_height - self.gap_size - 120)
        self.color = (34, 177, 76)
        self.scored = False

    @property
    def top_rect(self):
        return pygame.Rect(self.x, 0, self.width, self.gap_y)

    @property
    def bottom_rect(self):
        return pygame.Rect(
            self.x,
            self.gap_y + self.gap_size,
            self.width,
            self.screen.get_height() - (self.gap_y + self.gap_size),
        )

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.top_rect)
        pygame.draw.rect(self.screen, self.color, self.bottom_rect)

        top_cap = pygame.Rect(self.x - 6, self.gap_y - 20, self.width + 12, 20)
        bottom_cap = pygame.Rect(
            self.x - 6,
            self.gap_y + self.gap_size,
            self.width + 12,
            20,
        )
        pygame.draw.rect(self.screen, (40, 160, 70), top_cap)
        pygame.draw.rect(self.screen, (40, 160, 70), bottom_cap)

    def update(self, dt: float):
        self.x -= self.speed * dt

    def collides_with(self, bird_obj):
        "circle to rect collition"
        bird_left = bird_obj.pos.x - bird_obj.radius
        bird_right = bird_obj.pos.x + bird_obj.radius
        bird_top = bird_obj.pos.y - bird_obj.radius
        bird_bottom = bird_obj.pos.y + bird_obj.radius

        if bird_right < self.x or bird_left > self.x + self.width:
            return False

        if bird_top < self.gap_y or bird_bottom > self.gap_y + self.gap_size:
            return True

        return False