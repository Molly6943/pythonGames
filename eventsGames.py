import pygame,sys
pygame.init()
screen = pygame.display.set_mode([640,480])
background = pygame.Surface(screen.get_size())
background.fill([255,255,255])
clock = pygame.time.Clock()
delay = 100
interval = 50
pygame.key.set_repeat(delay,interval)
class Ball(pygame.sprite.Sprite):
    def __init__(self,image_file,speed,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = location
        self.speed = speed
    def move(self):
        if self.rect.left <= screen.get_rect().left or self.rect.right >= screen.get_rect().right:
            self.speed[0] = - self.speed[0]
        newpos = self.rect.move(self.speed)
        self.rect = newpos

myball = Ball("./bg_img/no.png",[10,0],[20,20])
held_town = False
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                myball.rect.top = myball.rect.top - 10
            elif event.key == pygame.K_DOWN:
                myball.rect.top = myball.rect.top + 10
        elif event.type == pygame.MOUSEBUTTONDOWN:
            held_town = True
        elif event.type == pygame.MOUSEBUTTONUP:
            held_town = False
        elif event.type == pygame.MOUSEMOTION:
            if held_town:
                myball.rect.center = event.pos
    clock.tick(10)
    screen.blit(background,[0,0])
    myball.move()
    screen.blit(myball.image,myball.rect)
    pygame.display.flip()
