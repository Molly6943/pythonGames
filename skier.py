import pygame, sys, random

skier_images = ["./bg_img/skier_down.png", "./bg_img/skier_right1.png", "./bg_img/skier_right2.png",
                 "./bg_img/skier_left2.png", "./bg_img/skier_left1.png"]

class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./bg_img/skier_down.png")
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.angle = 0

    def turn(self, direction):
        self.angle = self.angle + direction
        if self.angle < -2:  self.angle = -2
        if self.angle >  2:  self.angle =  2
        center = self.rect.center
        self.image = pygame.image.load(skier_images[self.angle])
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed = [self.angle, 6 - abs(self.angle) * 2]
        return speed

    def move(self, speed):
        self.rect.centerx = self.rect.centerx + speed[0]
        if self.rect.centerx < 20:  self.rect.centerx = 20
        if self.rect.centerx > 620: self.rect.centerx = 620

class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self, image_file, location, type):
        pygame.sprite.Sprite.__init__(self)
        self.image_file = image_file
        self.image = pygame.image.load(image_file)
        self.location = location
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type
        self.passed = False

    def scroll(self, terrainPos):
        self.rect.centery = self.location[1] - terrainPos

def create_map(start, end):
    obstacles = pygame.sprite.Group()
    locations = []
    gates = pygame.sprite.Group()
    for i in range(10):
        row = random.randint(start, end)
        col = random.randint(0, 9)
        location  = [col * 64 + 20, row * 64 + 20]
        if not (location in locations):
            locations.append(location)
            type = random.choice(["tree", "flag"])
            if type == "tree": img = "./bg_img/skier_tree.png"
            elif type == "flag":  img = "./bg_img/skier_flag.png"
            obstacle = ObstacleClass(img, location, type)
            obstacles.add(obstacle)
    return obstacles

def animate():
    screen.fill([255, 255, 255])
    pygame.display.update(obstacles.draw(screen))
    screen.blit(skier.image, skier.rect)
    screen.blit(score_text, [10, 10])
    pygame.display.flip()

def updateObstacleGroup(map0, map1):
    obstacles = pygame.sprite.Group()
    for ob in map0:  obstacles.add(ob)
    for ob in map1:  obstacles.add(ob)
    return obstacles

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("./bg_music/bg_music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
screen = pygame.display.set_mode([640,640])
clock = pygame.time.Clock()
skier = SkierClass()
speed = [0, 6]
map_position = 0
points = 0
map0 = create_map(20, 29)
map1 = create_map(10, 19)
activeMap = 0

obstacles = updateObstacleGroup(map0, map1)

font = pygame.font.Font(None, 50)

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = skier.turn(-1)
            elif event.key == pygame.K_RIGHT:
                speed = skier.turn(1)
    skier.move(speed)
    map_position += speed[1]

    if map_position >=640 and activeMap == 0:
        activeMap = 1
        map0 = create_map(20, 29)
        obstacles = updateObstacleGroup(map0, map1)
    if map_position >=1280 and activeMap == 1:
        activeMap = 0
        for ob in map0:
            ob.location[1] = ob.location[1] - 1280
        map_position = map_position - 1280
        map1 = create_map(10, 19)
        obstacles = updateObstacleGroup(map0, map1)

    for obstacle in obstacles:
        obstacle.scroll(map_position)

    hit =  pygame.sprite.spritecollide(skier, obstacles, False)
    if hit:
        if hit[0].type == "tree" and not hit[0].passed:
            points = points - 100
            skier.image = pygame.image.load("./bg_img/skier_crash.png")
            animate()
            pygame.time.delay(1000)
            skier.image = pygame.image.load("./bg_img/skier_down.png")
            skier.angle = 0
            speed = [0, 6]
            hit[0].passed = True
        elif hit[0].type == "flag" and not hit[0].passed:
            points += 10
            obstacles.remove(hit[0])                 

    score_text = font.render("Score: " +str(points), 1, (0, 0, 0))
    animate()
