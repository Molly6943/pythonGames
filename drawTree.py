import pygame,sys
pygame.init()
dots = [[221, 432],[225, 331],[133, 342],[141, 310],[51, 230],[74,217],[58,153],[114,164],[123,135],[176,190],[159,77],
[193,93],[230,28],[267,93],[301,77],[284,190],[327,135],[336,164],[402,153],[386,217],[409,230],[319,310],[327,342],
[233,311],[237,432]]
screen = pygame.display.set_mode([640,480])
screen.fill([225,225,225])
pygame.draw.lines(screen,[255,0,0],True,dots,2)
pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
