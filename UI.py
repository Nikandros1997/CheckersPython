import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect

TILE_SIZE = 60
TOKEN_SIZE = 50

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont('Courier', font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        super().__init__()

        self.mouse_over = False

        default_image = create_surface_with_text(text, font_size, text_rgb, bg_rgb)

        highlighted_image = create_surface_with_text(text, font_size * 1.2, text_rgb, bg_rgb)

        self.images = [
            default_image,
            highlighted_image
        ]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position)
        ]

        self.action = action

    @property
    def image(self):
        return self.images[1] if self.mouse_over and self.action else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over and self.action else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):

            self.mouse_over = True

            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class UIToken(pygame.sprite.Sprite):

    def __init__(self, x, y, image, token):
        super(UIToken, self).__init__()
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (TOKEN_SIZE, TOKEN_SIZE))
        self.clicked = False
        self.rect = self.image.get_rect()
        self.previousX = -1
        self.previousY = -1
        self.x = x
        self.y = y
        self.locate_token()
        self.token = token

    def move_token(self, x, y):

        if x < TOKEN_SIZE / 2:
            x = TOKEN_SIZE / 2

        if y < TOKEN_SIZE / 2:
            y = TOKEN_SIZE / 2

        if x > 8 * TILE_SIZE - TOKEN_SIZE / 2:
            x = 8 * TILE_SIZE - TOKEN_SIZE / 2

        if y > 8 * TILE_SIZE - TOKEN_SIZE / 2:
            y = 8 * TILE_SIZE - TOKEN_SIZE / 2

        self.rect.x = x - TOKEN_SIZE / 2
        self.rect.y = y - TOKEN_SIZE / 2

        self.x = int(x / TILE_SIZE)
        self.y = int(y / TILE_SIZE)

    def locate_token(self):

        self.rect.x = self.x * TILE_SIZE + (TILE_SIZE - TOKEN_SIZE) / 2
        self.rect.y = self.y * TILE_SIZE + (TILE_SIZE - TOKEN_SIZE) / 2

        if self.x == self.previousX and self.y == self.previousY:
            return -1, -1
        move = (self.previousX, 7 - self.previousY), (int(self.rect.x / TILE_SIZE), 7 - int(self.rect.y / TILE_SIZE))
        self.previousX = self.x
        self.previousY = self.y

        return move
