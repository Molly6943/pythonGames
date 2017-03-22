import pygame,sys,random
from pygame.locals import *
class MyBallClass(pygame.sprite.Sprite):
    def __init__(self,image_file,location,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = location
        self.speed = speed
    def move(self):
        global points,score_text
        self.rect = self.rect.move(self.speed)
        print self.speed
        if self.rect.left < 0 or self.rect.right > screen.get_width():
            self.speed[0] = - self.speed[0]
            hit_wall.play()
        if self.rect.top <= 0:
            points = points + 1
            if self.speed[1] < 0:
                self.speed[1] = random.randint(5,10)
            else:
                self.speed[1] = random.randint(-10,-5)

            score_text = font.render(str(points),1,(0,200,0))
            get_point.play()
        if self.rect.top >= screen.get_rect().bottom:
            hit_wall.stop()


class MyPaddleClass(pygame.sprite.Sprite):
    def __init__(self,location = [0,0]):
        pygame.sprite.Sprite.__init__(self)
        image_surface = pygame.surface.Surface([100,20])
        image_surface.fill([0,0,0])
        self.image = image_surface.convert()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = location


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("./bg_music/bg_music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
hit = pygame.mixer.Sound("./bg_music/hit_hanndel.wav")
hit.set_volume(0.60)

hit_wall = pygame.mixer.Sound("./bg_music/hit_wall.wav")
hit_wall.set_volume(0.20)

get_point = pygame.mixer.Sound("./bg_music/get_point.wav")
get_point.set_volume(0.30)

game_over = pygame.mixer.Sound("./bg_music/game_over.wav")
game_over.set_volume(0.40)

new_life = pygame.mixer.Sound("./bg_music/new_life.wav")
new_life.set_volume(0.40)

splat = pygame.mixer.Sound("./bg_music/splat.wav")
splat.set_volume(0.40)

screen = pygame.display.set_mode([640,480])
clock = pygame.time.Clock()
ball_speed = [random.randint(-10,5),random.randint(-5,10)]
myball = MyBallClass("./bg_img/pingpang.png",[50,50],ball_speed)
ballGroup = pygame.sprite.Group(myball)
paddle = MyPaddleClass([270,400])
lives = 3
points = 0

font = pygame.font.Font(None,50)
score_text = font.render(str(points),1,(0,200,0))
textpos = [10,10]
done = False

while 1:
    clock.tick(30)
    screen.fill([255,255,255])
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            paddle.rect.centerx = event.pos[0]

    if pygame.sprite.spritecollide(paddle,ballGroup,False):
        myball.speed[1] = - myball.speed[1]
        hit.play()

    myball.move()

    if not done:
        screen.blit(myball.image,myball.rect)
        screen.blit(paddle.image,paddle.rect)
        screen.blit(score_text,textpos)
        for i in range(lives):
            width = screen.get_width()
            screen.blit(myball.image,[width - 40 * i,20])
        pygame.display.flip()

    if myball.rect.top >= screen.get_rect().bottom:
        if not done:
            splat.play()
        lives = lives - 1
        if lives <= 0:
            if not done:
                pygame.time.delay(1000)
                game_over.play()
            final_text1 = "Game over!"
            final_text2 = "your final score is : " + str(points)
            ft1_font = pygame.font.Font(None,70)
            ft1_surf = font.render(final_text1,1,(200,0,0))
            ft2_font = pygame.font.Font(None,50)
            ft2_surf = font.render(final_text2,1,(0,200,0))
            screen.blit(ft1_surf,[screen.get_width() / 2 - ft1_surf.get_width() / 2,100])
            screen.blit(ft2_surf,[screen.get_width() / 2 - ft2_surf.get_width() / 2,200])
            pygame.display.flip()
            done = True
            pygame.mixer.music.fadeout(2000)
        else:
            pygame.time.delay(1000)
            new_life.play()
            myball.rect.topleft = [50,50]
            pygame.display.flip()
            pygame.time.delay(1000)
