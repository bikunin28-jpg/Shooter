#Создай собственный Шутер!
from random import randint
from pygame import *
from time import time as timer

font.init()
font1 = font.SysFont('Arial', 26)
fontfinish = font.SysFont('Arial', 60)
lost = 0
score = 0
life = 3
num_fire = 0
rel_time = False
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
mixer.init()
mixer.music.load('space.mp3')
mixer.music.set_volume(0.2)
mixer.music.play()

pew_pew = mixer.Sound('fire.ogg') 
pew_pew.set_volume(0.1)

class GameSprite(sprite.Sprite):
    def __init__(self, plr_image, plr_x, plr_y, plr_speed, plr_width, plr_height):
        super ().__init__()
        self.image = transform.scale(image.load(plr_image), (plr_width, plr_height))
        self.speed = plr_speed
        self.rect = self.image.get_rect()
        self.rect.x = plr_x
        self.rect.y = plr_y
        self.width = plr_width
        self.height = plr_height
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700-self.width: 
            self.rect.x +=  self.speed
        
    def fire(self):
        bullets.add(Bullet('bullet.png', self.rect.centerx - 8, self.rect.y, 15 , 15, 20))
        pew_pew.play()

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 700 - self.width)
            self.speed = randint(2, 7)
            lost += 1 

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 700 - self.width)
            self.speed = randint(1,5)


finihs = False       
game = True
player = Player('rocket.png', 350, 400, 10, 70, 100)
ufos = sprite.Group()
asteroids = sprite.Group()
for i in range(3):
    asteroids.add(Asteroid('asteroid.png', randint(0, 600), 0, randint(1,5), 70, 70))
for i in range(5):
    ufos.add(Enemy('ufo.png', randint(0, 600), 0, randint(2, 7), 100, 70))
bullets = sprite.Group()
while game:
    window.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    num_fire += 1
                if num_fire >=5 and rel_time == False:
                    rel_time = True
                    start_time = timer()
            if e.key == K_r:
                life = 3
                lost = 0
                score = 0
                rel_time = False
                num_fire = 0
                finihs = False
                for b in bullets:
                    b.kill()
                for u in ufos:
                    u.kill()
                for a in asteroids:
                    a.kill()
                for i in range(3):
                    asteroids.add(Asteroid('asteroid.png', randint(0, 600), 0, randint(1,5), 70, 70))
                for i in range(5):
                    ufos.add(Enemy('ufo.png', randint(0, 600), 0, randint(2, 7), 100, 70))
    if rel_time:
        now_time = timer()
        if now_time - start_time <3:
            rel_text = font1.render('Подождите, перезарядка', True,  (255, 0, 0))
            window.blit(rel_text, (250, 464))
        else:
            rel_time = False
            num_fire = 0
    player.reset()
    ufos.draw(window)
    bullets.draw(window)
    asteroids.draw(window)
    text_lost = font1.render('Пропущенно: ' + str(lost), 1, (255, 255, 255))
    text_score = font1.render('Счёт: ' + str(score), 1, (255, 255, 255))
    life_count = fontfinish.render(str(life), 1, (255, 255, 255))
    window.blit(text_lost, (10, 50))
    window.blit(text_score, (10, 20))
    window.blit(life_count, (670, 20))
    if not finihs:
        player.update()
        ufos.update()
        bullets.update()
        asteroids.update()
    else:
        window.blit(text_finish, (140, 190))
    if  lost >= 3 or life <=0:
        finihs = True
        text_finish = fontfinish.render('ВЫ ПРОИГРАЛИ!', True, (255, 0 , 0))
    if sprite.spritecollide(player, ufos, True):
        life -= 1
        ufos.add(Enemy('ufo.png', randint(0, 600), 0, randint(2, 7), 100, 70))
    if sprite.spritecollide(player, asteroids, True):
        life -= 1
        asteroids.add(Enemy('asteroid.png', randint(0, 600), 0, randint(1,5), 70, 70))

    sprites_list = sprite.groupcollide(ufos, bullets, True, True)
    for u in sprites_list:
        ufos.add(Enemy('ufo.png', randint(0, 600), 0, randint(2, 7), 100, 70))
        score += 1    
    if score >= 10:
        finihs = True
        text_finish = fontfinish.render('ВЫ ВЫИГРАЛИ!', True, (255, 255, 255))

    display.update()
    time.delay(30)