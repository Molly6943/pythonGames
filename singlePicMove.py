import pygame,sys
pygame.init()
screen = pygame.display.set_mode([640,480])
screen.fill([225,225,225])
my_ball = pygame.image.load("no.png")
x = 50
y = 50
x_speed = 5
y_speed = 10
for looper in range(1,200):
    screen.blit(my_ball,[x,y])
    pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.time.delay(80)
    pygame.draw.rect(screen,[225,225,225],[x,y,65,65],0)
    x = x + x_speed
    y = y + y_speed
    if x > screen.get_width() - 65 or x < 0:
        x_speed = - x_speed
    if y > screen.get_height() - 65 or y <0:
        y_speed = - y_speed
    if x > screen.get_width():
        x = 0
    if y > screen.get_height():
        y = 0
    screen.blit(my_ball,[x,y])
    pygame.display.flip()
