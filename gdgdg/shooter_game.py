from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, player_im, p_x, p_y, player_speed, s_x, s_y):
        super().__init__()
        self.image = transform.scale(image.load(player_im), (s_x, s_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= 8
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += 8
    def fire(self):
        bul = Bullet('bullet.png', self.rect.centerx, self.rect.top, 5, 18, 18)
        bullets.add(bul)

