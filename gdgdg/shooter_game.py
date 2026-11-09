from pygame import *
from random import randint
from time import time as timer
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

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(50, 650)
            lost = lost + 1
    def bul_coll(self):
        pass

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(50, 650)
    def bul_coll(self):
        pass

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

num_fire = 0
rel_time = False
lost = 0
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Space')   
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
fire = mixer.Sound('fire.ogg')
timer1 = time.Clock()
player = Player('rocket.png', 65, 425, 8, 70, 70)
monsters = sprite.Group()
comets = sprite.Group()
bullets = sprite.Group()
font.init()
fot = font.SysFont('Arial', 45)
fot_2 = font.SysFont('Arial', 150)
dead = 0
for i in range(8):
    monster = Enemy('ufo.png', randint(5, 650), -50, randint(1,3), 50, 50)
    monsters.add(monster)
for i in range(3):
    comet = Asteroid('asteroid.png', randint(5, 650), randint(-50, 100),randint(3,5), 70, 70)
    comets.add(comet)
finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    fire.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    real_time = True
                    clock1 = timer()
    if finish != True:
        check_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in check_list:
            dead += 1
            monster = Enemy('ufo.png', randint(5, 650), -50, randint(1,3), 50, 50)
            monsters.add(monster)
        sprites_list = sprite.spritecollide(player, monsters, False)
        comets_list = sprite.spritecollide(player, comets, False)
        window.blit(background,(0,0))
        if sprites_list != [] or lost >= 3 or comets_list != []:
            finish = True
            lose = fot_2.render('YOU LOSE', 1, (255, 0, 0))
            window.blit(lose, (100,200))
        if dead >= 10:
            finish = True
            win = fot_2.render('YOU WIN', 1, (0, 255, 0))
            window.blit(win, (100,200))
        if rel_time == True:
            clock_2 = timer()
            if clock_2 - clock1 >= 3:
                num_fire = 0
                rel_time = False
            else:
                reload1 = fot.render('Wait, reload...', 1, (150, 0, 0)) 
                window.blit(reload1, (260, 360))
        text = fot.render('Пропущено: ' + str(lost), 1, (255, 255, 255), (255,0,0))
        window.blit(text, (5,35))
        score = fot.render('Счёт: ' + str(dead), 1, (255,255,255), (0,255,0))
        window.blit(score, (5,0))
        player.update()
        player.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        comets.update()
        comets.draw(window)

    display.update()
    timer1.tick(60)
