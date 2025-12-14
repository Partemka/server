from time import time as timer
from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self,x,y,speed,w,h,path):
        super().__init__()
        self.speed = speed
        self.w = w
        self.h = h
        self.image = transform.scale(image.load(path),(self.w,self.h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x >= 5:
            self.rect.x -= self.speed 
        if keys_pressed[K_RIGHT] and self.rect.x <= 615:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(self.rect.x+33, self.rect.top-20 , 20, 15, 20, 'bullet.png')
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self,colliding):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.y = -40
            self.rect.x = randint(0,win_width-80)
            if colliding:
                lost +=1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -100:
            self.kill()


win_width = 700
win_height = 500
FPS = 60
game =True
font.init()
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
backgrtound = transform.scale(image.load('galaxy.jpg'),(win_width, win_height))
clock = time.Clock()

player = Player(100,400,10,80,100,'rocket.png')
monsters = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()
lost = 0
score = 0
if_fire = False
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 70)
win = font2.render('Ты победил', True, (255,255,255))
lose = font2.render('Ты проиграл', True, (255,255,255))
reloa = font1.render('Wait reload...', True, (255,0,0))

finish = False
rel_time = False
life = 3
num_shots = 0
for i in range(2):
    asteroid = Enemy(randint(0, win_width-80), -40, randint(1,5), 80, 50, 'asteroid.png')
    asteroids.add(asteroid)
for i in range(5):
    monster = Enemy(randint(0, win_width-80), -40, randint(1,5), 80, 50, 'ufo.png')
    monsters.add(monster)
while game:

    for g in event.get():

        if g.type == QUIT:
            game = False

        if g.type == KEYDOWN:

            if g.key == K_SPACE:
                
                if num_shots<5 and rel_time == False:
                    num_shots+=1
                    player.fire()

                if num_shots >= 5 and rel_time == False:
                    rel_time = True
                    start_time = timer()



    if not finish:
        window.blit(backgrtound,(0,0))
        collides = sprite.groupcollide(monsters, bullets, True, True)

        for i in collides:
            score+=1
            monster = Enemy(randint(0, win_width-80), -40, randint(1,5), 80, 50, 'ufo.png')
            monsters.add(monster)

        if score >= 10:
            finish = True

            window.blit(win, (200,200))
        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, asteroids, True):
            life -= 1

        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update(True)
        asteroids.draw(window)
        asteroids.update(False)
        bullets.draw(window)
        bullets.update()
        text1 = font1.render('Пропущено: '+ str(lost), True, (255,255,255))
        window.blit(text1, (10, 50))
        text2 = font1.render('Счет: '+str(score), True, (255,255,255))
        window.blit(text2, (10, 25))
        if life == 3:
            lifes = font2.render(str(life), True, (0,255,0))
        if life == 2:
            lifes = font2.render(str(life), True, (255,255,0))
        if life == 1:
            lifes = font2.render(str(life), True, (255,0,0))
        if life <=0 or  lost >= 3:
            finish = True
            window.blit(lose, (200,200))
        window.blit(lifes, (620,0))
        if rel_time:
            end_time = timer()
            if end_time - start_time >= 3:
                rel_time = False
                num_shots = 0
            else:
                window.blit(reloa,(200,500-40))
                

            

    display.update()
    time.delay(50)
